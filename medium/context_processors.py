from medium.models import Medium


def menu_links(request):
    links = Medium.objects.all()
    return dict(links=links)