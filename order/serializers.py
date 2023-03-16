# from rest_framework.serializers import ModelSerializer
# from .models import Order, Favorite


# class OrderSerializer(ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'


# class FavoriteSerializer(ModelSerializer):
#     class Meta:
#         model = Favorite
#         fields = '__all__'


from rest_framework import serializers
from .models import Order, OrderItem, Favorite

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True) # сюда бубдт попадать наши продукты и они будут являться поолями

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'total_sum', 'items']

    def create(self, validated_data):
        items = validated_data.pop('items')
        validated_data['author'] = self.context.get('user') # self.context['request'].user можно и так записать
        order = super().create(validated_data)
        total_sum = 0
        order_items = []
        for item in items:
            print(item)
            order_items.append(OrderItem(order=order, product=item['product'], quantity=item['quantity'])) # создаем объекты от ордер айтем
            total_sum += item['product'].price * item['quantity']
        OrderItem.objects.bulk_create(order_items)
        order.total_sum = total_sum
        order.save()
        return order


class FavoriteSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField(source='author.email')
    
    class Meta:
        model = Favorite
        fields = '__all__'