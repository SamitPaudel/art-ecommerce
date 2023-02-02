from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from accounts.models import Account
from tinymce.models import HTMLField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager

class PostCategory(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    description = models.TextField(default='description')

    class Meta:
        verbose_name_plural = 'PostCategories'
    def __str__(self):
        return self.title

    def get_url(self):
        return reverse("posts", kwargs={
            "slug":self.slug
        })

    @property
    def num_posts(self):
        return Post.objects.filter(categories=self).count()

    @property
    def last_post(self):
        return Post.objects.filter(categories=self).latest("date")

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = HTMLField()
    categories = models.ManyToManyField(PostCategory)
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation'
                                        )
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse("detail", kwargs={
            "slug":self.slug
        })
