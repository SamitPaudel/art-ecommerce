from .models import Post

def searchFunction(request):
    context = {}
    objects = None
    query = None
    posts = Post.objects.all()
    if "search" in request.GET:
        query= request.GET.get("q")
        seach_box = request.GET.get("search-box")
        if seach_box == "Descriptions":
            objects = posts.filter(content__icontains=query)
        else:
            objects = posts.filter(title__icontains=query)

    context = {
        "objects":objects,
        "query":query,
    }
    return context