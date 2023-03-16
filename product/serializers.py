from rest_framework.serializers import ModelSerializer
from .models import Product, Category
from review.models import Comment
from rest_framework import serializers
from review.serializers import RatingSerializer, CommentSerializer
from review.models import Rating
from django.db.models import Avg


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, price): # сначала всегда валидете(метод пишеим проверки как назыввается под каптом) а потом нащвание поля, которе необходимо проверить! и его передаем в качестве аргумента
        if price < 0:
            raise serializers.ValidationError('Цена не может быть отрицательной')
        return price

    def to_representation(self, instance): # добавляет поля к продукту (от куда брать какие поля)
        representation = super().to_representation(instance)
        # representation['ratings'] = RatingSerializer(instance.ratings.all(), many=True).data # получили все рейтинги от каждого пользователя!! # (дз вывести усредненный рейтинг в продукатах, вывсети комментарии к этому продукту)
        # representation['ratings'] = instance.ratings.aggregate(Avg('rating'))['rating__avg'] # средний рейтинг от всех пользователей
        # representation['comments'] = CommentSerializer(Comment.objects.filter(product=instance.pk),many=True).data # прикрутили показ комментариев к продукту
        representation['comments'] = [i.body for i in instance.comments.all()]
        print(CommentSerializer(instance.comments.all(),many=True).data)
        representation['ratings'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        representation['likes_count'] = instance.likes.count()
        return representation
        