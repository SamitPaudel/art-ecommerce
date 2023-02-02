from django.shortcuts import render, get_object_or_404
from .models import Post, PostCategory
from .utils import update_views

# Create your views here.
def home(request):
    forums = PostCategory.objects.all()
    context = {
        "forums": forums
    }
    return render(request, "forum_home.html", context)


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        "post": post
    }
    update_views(request, post)
    return render(request, "forum_detail.html", context)

def posts(request, slug):
    post_category = get_object_or_404(PostCategory, slug=slug)
    posts = Post.objects.filter(approved=True, categories=post_category)

    context = {
        "posts":posts
    }

    return render(request, "posts.html", context)

