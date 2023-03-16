from rest_framework import serializers
from .models import Comment, Like, Rating, LikeComment
from django.db.models import Avg


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email') # поле автора для чтения а не для заполнения

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request') # получаем контекст с реквеста
        user = request.user # юзер который отпрправил запрос
        comment = Comment.objects.create(author=user, **validated_data)
        return comment

# class CommentDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
        # exclude = ['author']

    def to_representation(self, instance): # добавляет поля к продукту (от куда брать какие поля)
        representation = super().to_representation(instance)
        representation['ratings'] = RatingSerializer(instance.ratings.all(), many=True).data # получили все рейтинги от каждого пользователя!! # (дз вывести усредненный рейтинг в продукатах, вывсети комментарии к этому продукту)
        representation['ratings'] = instance.ratings.aggregate(Avg('rating'))['rating__avg'] # средний рейтинг от всех пользователей
        representation['comments'] = CommentSerializer(Comment.objects.filter(product=instance.pk),many=True).data # прикрутили показ комментариев к продукту
        representation['comments'] = [i.body for i in instance.comments.all()]
        print(CommentSerializer(instance.comments.all(),many=True).data)
        representation['ratings'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        representation['likes_count'] = instance.likes.count()
        return representation



class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    product = serializers.ReadOnlyField()
    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request') # получаем контекст с реквеста (мы вытаскиваем из сути всего нашего проекта) контекст - это позволянет на вытащить реквест
        user = request.user # юзер который отпрправил запрос
        like = Like.objects.create(author=user, **validated_data)
        return like


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    class Meta:
        model = Rating
        fields = '__all__'

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError('рейтиенг не может быть меньще 0 и больше 5')
        return rating

    def validate_product(self, product):
        if self.Meta.model.objects.filter(product=product).exists():
            raise serializers.ValidationError('вы уже оставляли рейтинг')
        return product

    def create(self, validate_data):
        request = self.context.get('request')
        user = request.user
        rating = Rating.objects.create(author=user, **validate_data)
        return rating

    # def update(self, instance, validated_data):
    #     instance.rating = validated_data.get('rating')
    #     instance.save()
    #     return super().update(instance, validated_data)

    # def validate_rating(self, rating):
    #     if rating < 0:
    #         raise serializers.ValidationError('Рейтинг должен быть больше 0')
    #     return rating

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     user = request.user
    #     comment = Rating.objects.create(author=user, **validated_data)
    #     return comment


class LikeCommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    comment = serializers.ReadOnlyField()

    class Meta:
        model = LikeComment
        fields = '__all__'
        
    def create(self, validated_data):
        request = self.context.get('request') # получаем контекст с реквеста
        user = request.user # юзер который отпрправил запрос
        like_comment = LikeComment.objects.create(author=user, **validated_data)
        return like_comment



    

    