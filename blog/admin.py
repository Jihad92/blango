from django.contrib import admin
from django.forms import Textarea, TextInput
from django.db import models
from .models import (
    Tag,
    Post,
    Comment,
    AuthorProfile
)
from django.contrib.contenttypes.admin import GenericTabularInline

# Register your models here.
class TagAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(
                attrs={
                    'size': 100
                }
            )
        }
    }

class CommentAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(
                attrs={
                    'rows': 8,
                    'cols': 100,
                    'style': 'resize: none'
                }
            )
        }
    }

class CommentInline(GenericTabularInline):
    model = Comment
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(
                attrs={
                    'rows': 8,
                    'cols': 100,
                    'style': 'resize: none'
                }
            )
        }
    }

class PostAdmin(admin.ModelAdmin):
    list_display = ('slug', 'published_at')
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(
                attrs={
                    'size': 100
                }
            )
        },
        models.TextField: {
            'widget': Textarea(
                attrs={
                    'rows': 8,
                    'cols': 100,
                    'style': 'resize: none'
                }
            )
        }
    }
    prepopulated_fields = {
        'slug': ('title',),
    }
    inlines = [
        CommentInline,
    ]

admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(AuthorProfile)