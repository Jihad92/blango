from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from versatileimagefield.fields import VersatileImageField, PPOIField

# Create your models here.


class Tag(models.Model):
    value = models.CharField(max_length=100, unique=True)
    
    class Meta:
        ordering = ["value"]

    def __str__(self):
        return self.value


class Comment(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.creator}.comment.{self.id}"


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    summary = models.TextField(max_length=500)
    content = models.TextField()

    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    comments = GenericRelation(Comment)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True, db_index=True)

    hero_image = VersatileImageField(upload_to="hero_images", ppoi_field="ppoi", null=True, blank=True)
    ppoi = PPOIField(null=True, blank=True)
    
    class Meta:
        ordering = ["slug"]
    
    def __str__(self):
        return self.title


class AuthorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField()

    def __str__(self):
        return f"{self.__class__.__name__} object for {self.user}"
