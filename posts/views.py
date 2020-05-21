from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import PostForm, CreateCommentForm
from .models import Post, SavedPosts, PostViews, Comment, Like
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import services

@login_required
def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
        return HttpResponseRedirect('/profile')
    else:
        return render(request, 'posts/create.html', {'title': 'Создать пост', 'form': form})


class PostsView(ListView):
    model = Post
    paginate_by = 4
    template_name = 'posts/news.html'
    ordering = ['-created_date']


def get_post(request, pk):
    if request.method == 'GET':
        post_found = Post.objects.get(pk=pk)
        if post_found is None:
            return HttpResponseRedirect('/news')

        views_count = PostViews.objects.filter(post=post_found).count()

        if request.user.is_authenticated:
            views_found = PostViews.objects.filter(user=request.user, post=post_found)
            if len(views_found) == 0:
                PostViews(post=post_found, user=request.user).save()

        form = CreateCommentForm()
        comments = Comment.objects.all().order_by('-created_date')
        likes_count = Like.objects.filter(post=post_found).count()

        has_liked = len(Like.objects.filter(post=post_found, author=request.user)) != 0

        return render(request, 'posts/post.html', {
            'object': post_found,
            'title': post_found.title,
            'views_count': views_count,
            'comments': comments,
            'form': form,
            'likes_count': likes_count,
            'has_liked': has_liked
        })


@login_required
def create_comment(request, pk):
    if request.method == 'POST':
        post_found = Post.objects.get(pk=pk)
        if post_found is None:
            return HttpResponseRedirect('/news')
        comment = CreateCommentForm(request.POST).save(commit=False)
        comment.author = request.user
        comment.post = post_found
        comment.save()
        return HttpResponseRedirect(f'/news/{pk}')


@login_required
def save_post(request, pk):
    post = Post.objects.get(pk=pk)
    if post is not None:
        found = SavedPosts.objects.filter(post=post, author=request.user)

        if len(found) is 0:
            saved = SavedPosts(author=request.user, post=post)
            saved.save()
        return HttpResponseRedirect('/saved')


class SavedView(LoginRequiredMixin, ListView):
    model = SavedPosts
    paginate_by = 4
    template_name = 'posts/saved.html'
    ordering = ['-post.created_date']

    def get_queryset(self):
        return SavedPosts.objects.filter(author=self.request.user)


def search_handler(request):
    search_query = request.GET.get('search_query', '')
    posts = services.find_post(search_query=search_query)
    return render(request, 'posts/search.html', {
        'posts': posts,
        'title': 'Поиск'
    })


@login_required
def like_post(request, pk):
    post = Post.objects.get(pk=pk)
    if post is not None:
        found = Like.objects.filter(post=post, author=request.user)

        if len(found) is 0:
            saved = Like(author=request.user, post=post)
            saved.save()
        return HttpResponseRedirect(f'/news/{pk}')

