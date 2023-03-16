from django.urls import path, include
# from .views import CommentView, CommentDetailView
from rest_framework.routers import DefaultRouter
from .views import RatingViewSet, CommentViewSet#, LikeCommentViewSet,  LikeViewSet


router = DefaultRouter() #
router.register('rating', RatingViewSet)
router.register('comments', CommentViewSet)
# router.register('likecomment', LikeCommentViewSet)
# router.register('like', LikeViewSet)

urlpatterns = [
    # path('comments/', CommentView.as_view()),
    # path('comments/<int:pk>/', CommentDetailView.as_view()),
    path('', include(router.urls)),
]