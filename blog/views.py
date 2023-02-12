from datetime import timedelta
from django.http import Http404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from blango_auth.models import User
from .api.serializers import (
    PostSerializer,
    UserSerializer,
    PostDetailSerializer,
    TagSerializer,
)
from .api.filters import PostFilterSet
from .api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject
from .forms import CommentForm
from .models import Post, Tag

# Create your views here.


def index(request):
    posts = Post.objects.filter(published_at__lte=timezone.now()).select_related(
        "author"
    )
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
class UserDetail(generics.RetrieveAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @method_decorator(cache_page(120))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    # @method_decorator(cache_page(300))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(300))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(methods=["GET"], detail=True, name="Posts with the tag")
    def posts(self, request, pk=None):
        tag = self.get_object()

        page = self.paginate_queryset(tag.posts.all())
        if page is not None:
            post_serializer = PostSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(post_serializer.data)

        post_serializer = PostSerializer(
            tag.posts, many=True, context={"request": request}
        )
        return Response(post_serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    # permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    filterset_class = PostFilterSet
    ordering_fields = ["published_at", "author", "title", "slug"]

    # @method_decorator(cache_page(300))
    @method_decorator(vary_on_headers("Authorization"))
    @method_decorator(vary_on_cookie)
    @action(methods=["GET"], detail=False, name="Posts by the logged in user")
    def mine(self, request):
        if request.user.is_anonymous:
            raise PermissionDenied("You must be logged in to see which posts are yours")
        posts = self.get_queryset().filter(author=request.user)

        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = PostSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)

    # @method_decorator(cache_page(120))
    @method_decorator(vary_on_headers("Authorization", "Cookie"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return PostSerializer
        return PostDetailSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.is_anonymous:
            queryset = self.queryset.filter(published_at__lte=timezone.now())
        if not self.request.user.is_staff:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(
                Q(published_at__lte=timezone.now()) | Q(author=self.request.user)
            )
        time_period_name = self.kwargs.get("period_name")
        if not time_period_name:
            return queryset
        if time_period_name == "new":
            return queryset.filter(
                published_at__gte=timezone.now() - timedelta(hours=1)
            )
        elif time_period_name == "today":
            return queryset.filter(published_at__date=timezone.now().date())
        elif time_period_name == "week":
            return queryset.filter(published_at__gte=timezone.now() - timedelta(days=7))
        raise Http404(
            f"Time period {time_period_name} is not valid, should be 'new', 'today' or 'week'"
        )
