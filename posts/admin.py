from django.contrib import admin
from .models import Post, Comment, Category, Tag, Like, PostViews, SavedPosts
from django.db.models import Q

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(PostViews)
admin.site.register(SavedPosts)


class SearchFilter(admin.AllValuesFieldListFilter):
    parameter_name = 'search'
    title = 'Поиск'

    def queryset(self, request, queryset):
        if self.value() is not None:
            search = self.value()
            return queryset.filter(
                Q(title=search) |
                Q(user__username=search)
            )
