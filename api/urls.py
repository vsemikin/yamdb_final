from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router = DefaultRouter()
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="Review"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="Comment",
)
router.register(r"categories", CategoryViewSet, basename="Category")
router.register(r"genres", GenreViewSet, basename="Genre")
router.register(r"titles", TitleViewSet, basename="Titles")

urlpatterns = [
    # Custom categories endpoints
    path(
        "v1/categories/",
        CategoryViewSet.as_view({"get": "list", "post": "create"}),
        name="categories",
    ),
    path(
        "v1/categories/<slug:slug>/",
        CategoryViewSet.as_view({"delete": "destroy"}),
        name="categories_delete",
    ),
    # Custom genres endpoints
    path(
        "v1/genres/",
        GenreViewSet.as_view({"get": "list", "post": "create"}),
        name="genres",
    ),
    path(
        "v1/genres/<slug:slug>/",
        GenreViewSet.as_view({"delete": "destroy"}),
        name="genres_delete",
    ),
    path("v1/", include(router.urls)),
    path("v1/", include("users.urls")),
]
