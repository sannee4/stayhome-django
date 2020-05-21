from .views import create_post, SavedView, PostsView, get_post, save_post, create_comment, search_handler, like_post
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('create/', create_post),
    path('news/', PostsView.as_view()),
    path('news/<int:pk>', get_post),
    path('save/<int:pk>', save_post),
    path('news/<int:pk>/comment', create_comment),
    path('saved', SavedView.as_view()),
    path('search', search_handler),
    path('like/<int:pk>', like_post)
]
