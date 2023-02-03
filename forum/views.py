from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from accounts.models import Account
from .forms import PostForm
from .models import Post, PostCategory, Comment, Reply
from .utils import update_views

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def home(request):
    forums = PostCategory.objects.all()
    context = {
        "forums": forums
    }
    return render(request, "forum_home.html", context)


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    author = Account.objects.get(username=request.user.username)

    if "comment-form" in request.POST:
        comment = request.POST.get("comment")
        new_comment, created = Comment.objects.get_or_create(user=author, content=comment)
        post.comments.add(new_comment.id)

    if "reply-form" in request.POST:
        reply = request.POST.get("reply")
        commenr_id = request.POST.get("comment-id")
        comment_obj = Comment.objects.get(id=commenr_id)
        new_reply, created = Reply.objects.get_or_create(user=author, content=reply)
        comment_obj.replies.add(new_reply.id)
        return redirect("forum_detail", slug=post.slug)

    context = {
        "post": post
    }
    update_views(request, post)
    return render(request, "forum_detail.html", context)

def posts(request, slug):
    post_category = get_object_or_404(PostCategory, slug=slug)
    posts = Post.objects.filter(approved=True, categories=post_category)
    paginator = Paginator(posts, 10)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "posts":posts,
        "forum": post_category,
    }

    return render(request, "posts.html", context)

@login_required
def create_post(request):
    context = {}
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            print("\n\n its valid")
            author = Account.objects.get(username=request.user.username) # or use any other unique identifier for Account model
            new_post = form.save(commit=False)
            new_post.user = author
            new_post.save()
            form.save_m2m()
            return redirect("home")
    context.update({
        "form": form,
        "title": "Create New Post"
    })
    return render(request, "create_post.html", context)


