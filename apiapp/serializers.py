from rest_framework import serializers
from posts import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .validators import validate_username


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Incorrect email or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'last_login',
            'email',
            'username',
            'password'
        )
        read_only_fields = ('last_login', 'is_active', 'joined_at')
        extra_kwargs = {
            'password': {'required': True, 'write_only': True},
            'name': {'required': True}
        }

    @staticmethod
    def validate_email(value):
        return validate_username(value)

    def create(self, validated_data):
        return User.objects.create_user(
                    validated_data.pop('email'),
                    validated_data.pop('password'),
                    **validated_data
                )


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ['title', 'content', 'created_date', 'author', 'tags', 'category', 'comments']


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ['title', 'content', 'created_date', 'author', 'tags', 'category', 'comments']
        read_only_fields = ('author',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['author', 'post', 'content']


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        exclude = ['author']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = ['post', 'author']


class CreateLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        exclude = ['author']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ['name']
