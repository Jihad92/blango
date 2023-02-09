from django.urls import path, include
from rest_framework.authtoken import views as auth_views
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("post/<slug>", views.post_detail, name="blog-post-detail"),
    # api
    path("posts", views.PostList.as_view(), name="post-list"),
    path("posts/<int:pk>", views.PostDetail.as_view(), name="post-detail"),
    path("token-auth/", auth_views.obtain_auth_token),
]
