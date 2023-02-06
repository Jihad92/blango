from django.contrib import admin
from django.forms import Textarea, TextInput
from django.db import models
from .models import (
    Tag,
    Post
)

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

admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)