from rest_framework import routers
from . import viewsets
from . import views

router = routers.DefaultRouter()
router.register('posts', viewsets.PostsViewSet)
router.register('categories', viewsets.CategoryViewSet)
router.register('comments', viewsets.CommentsViewSet)
router.register('likes', viewsets.LikeViewSet)
router.register('tags', viewsets.TagsViewSet)