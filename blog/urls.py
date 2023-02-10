from django.urls import path, include, re_path
from rest_framework.authtoken import views as auth_views
from rest_framework.routers import DefaultRouter
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from . import views


router = DefaultRouter()
router.register("tags", views.TagViewSet)
router.register("posts", views.PostViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Blango API",
        default_version="v1",
        description="API for Blango Blog",
    ),
    url=f"http://127.0.0.1:8000/",
    public=True,
)

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<slug>", views.post_detail, name="blog-post-detail"),
    # api
    path("", include(router.urls)),
    path("users/<str:email>", views.UserDetail.as_view(), name="api_user_detail"),
    path("token-auth/", auth_views.obtain_auth_token),
    # swagger api
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
