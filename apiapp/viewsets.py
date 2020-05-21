from rest_framework import viewsets
from . import serializers
from posts import models
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class PostsViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostsSerializer
    ordering = ('-created_date',)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = []
        if self.action != 'list' or self.action != 'get':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if hasattr(self.request, 'method'):
            if self.request.method == 'GET':
                return serializers.PostsSerializer
            else:
                return serializers.CreatePostSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            return models.Post.objects.all()
        else:
            return models.Post.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.update(author=self.request.user)

    def perform_delete(self, serializer):
        serializer.delete(author=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_permissions(self):

        permission_classes = []
        if self.action != 'list' or 'get':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    ordering = ('-created_date',)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = []
        if self.action != 'list' or 'get':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if hasattr(self.request, 'method'):
            if self.request.method == 'GET':
                return serializers.CommentSerializer
            else:
                return serializers.CreateCommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.update(author=self.request.user)

    def perform_delete(self, serializer):
        serializer.delete(author=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = models.Like.objects.all()
    serializer_class = serializers.LikeSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = []
        if self.action != 'list' or 'get':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if hasattr(self.request, 'method'):
            if self.request.method == 'GET':
                return serializers.LikeSerializer
            else:
                return serializers.CreateLikeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.update(author=self.request.user)

    def perform_delete(self, serializer):
        serializer.delete(author=self.request.user)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = []
        if self.action != 'list' or 'get':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
