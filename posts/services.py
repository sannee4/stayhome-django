from .models import Post
from django.db.models import Q


def find_post(search_query=None):
    return Post.objects.filter(
        Q(title__contains=search_query) |
        Q(slug__contains=search_query) |
        Q(author__username__contains=search_query) |
        Q(content__contains=search_query) |
        Q(category__name=search_query)
    )
