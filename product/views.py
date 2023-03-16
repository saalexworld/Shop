from rest_framework.viewsets import ModelViewSet
from .models import Product, Category
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.decorators import action
from review.serializers import LikeSerializer
from review.models import Like
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAdminUser, AllowAny
from order.serializers import FavoriteSerializer
from order.models import Favorite


class PermissionMixin:
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permissions = [IsAdminUser]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]


class CategoryViewSet(PermissionMixin, ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

class ProductViewSet(PermissionMixin, ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['category', 'in_stock']
    search_fields = ['price']
    
    @action(methods=['POST'], detail=True)   # detail=True - какое количнество элементов, тру - все
    def like(self, request, pk=None):
        product = self.get_object()
        author = request.user # создадим автора из реквеста чтобы поле было автоматически заполнено
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data)
            try:
                like = Like.objects.get(product=product, author=author) # чтобы автора отслежаваить
                like.delete()
                # like.is_liked = not like.is_liked
                # like.save()
                message = 'disliked' # выводи сообщение о лайке или дизлайке
            except Like.DoesNotExist:
                Like.objects.create(product=product, is_liked=True, author=author) # если лайка нет, то создадим его
                message = 'liked'
            return Response(message, status=200)

    @action(methods=['POST'], detail=True)# detail=True -одлин объект
    def favorite(self, request, pk=None):
        product = self.get_object()
        author = request.user
        serializer = FavoriteSerializer(data=request.data) # сериализуем наши данные (из джейсона в  питон файл)
        if serializer.is_valid(raise_exception=True):
            try:
                favorite = Favorite.objects.get(product=product, author=author)
                favorite.delete()
            except Favorite.DoesNotExist:
                Favorite.objects.create(product=product, author=author, is_favorite=True)
                message = 'deleted from favotites'
            return Response(message, status=200)



            