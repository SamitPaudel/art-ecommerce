from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from accounts.models import Account
from .forms import PostForm, CommentForm, ReplyForm
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


from django.shortcuts import render, get_object_or_404
from .models import Post


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    for comment in comments:
        comment.replies.set(comment.replies.all())
    form = CommentForm()  # initialize form variable
    reply_form = ReplyForm()  # initialize reply_form variable
    if request.method == 'POST':
        print("Request is POST")
        if 'comment_id' in request.POST:
            comment_id = request.POST.get('comment_id')
            form = CommentForm(request.POST)
            if form.is_valid():
                print('Comment form is valid:', form.cleaned_data['content'])
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.parent_comment_id = comment_id
                comment.save()
                form = CommentForm()
        elif 'reply_id' in request.POST:
            reply_id = request.POST.get('reply_id')
            form = ReplyForm(request.POST)
            if form.is_valid():
                print('Reply form is valid:', form.cleaned_data['content'])
                reply = form.save(commit=False)
                reply.user = request.user
                reply.comment_id = reply_id
                reply.save()
                reply_form = ReplyForm()  # move initialization of reply_form here
    else:
        form = CommentForm()
        print("Enters else block")
    # move initialization of reply_form outside of the else block
    reply_form = ReplyForm()

    return render(request, 'forum_detail.html',
                  {'post': post, 'comments': comments, 'form': form, 'reply_form': reply_form})


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
        "posts": posts,
        "forum": post_category,
    }

    return render(request, "posts.html", context)


@login_required
def create_post(request):
    context = {}
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            author = Account.objects.get(
                username=request.user.username)  # or use any other unique identifier for Account model
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


def search_result(request):
    return render(request, "search_results.html")
