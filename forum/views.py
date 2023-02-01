from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "forum_home.html")

def detail(request):
    return render(request, "forum_detail.html")

def posts(request):
    return render(request, "posts.html")

