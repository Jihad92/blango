from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics

from blango_auth.models import User
from .api.serializers import PostSerializer, UserSerializer
from .api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject
from .forms import CommentForm
from .models import Post

# Create your views here.


def index(request):
    posts = Post.objects.filter(published_at__lte=timezone.now()).select_related('author')
    return render(request, "blog/index.html", {"posts": posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    return render(
        request,
        "blog/post-detail.html",
        {
            "post": post,
            "comment_form": comment_form,
        },
    )

# api
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]

class UserDetail(generics.RetrieveAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer
