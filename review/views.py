from rest_framework import generics, viewsets
from .models import Comment, Like, Rating, LikeComment
from .serializers import CommentSerializer, RatingSerializer, LikeSerializer, LikeCommentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAuthorOrReadOnly

class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorOrReadOnly]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]



class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(methods=['POST'], detail=True)   # detail=True - какое количнество элементов, тру - все
    def like(self, request, pk=None):
        comment = self.get_object()
        author = request.user # создадим автора из реквеста
        serializer = LikeCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data)
            try:
                like = LikeComment.objects.get(comment=comment, author=author) # чтобы автора отслежаваить
                like.delete()
                # like.is_liked = not like.is_liked
                # like.save()
                message = 'disliked' # выводи сообщение о лайке или дизлайке
            except LikeComment.DoesNotExist:
                LikeComment.objects.create(comment=comment, is_liked=True, author=author) # если лайка нет, то создадим егоc
                message = 'liked'
            return Response(message, status=200)


# class CommentDetailView(generics.RetrieveUpdateDestroyAPIView): # обновдление, удаление, обзор
    # queryset = Comment.objects.all()
    # serializer_class = CommentSerializer


class RatingViewSet(PermissionMixin, ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer



# количество лайков на комментарии

# class LikeViewSet(PermissionMixin,ModelViewSet):
#     queryset = Like.objects.all()
#     serializer_class = LikeSerializer


# class LikeCommentViewSet(PermissionMixin,ModelViewSet):
#     queryset = LikeComment.objects.all()
#     serializer_class = LikeCommentSerializer