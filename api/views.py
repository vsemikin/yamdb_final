import django_filters
from django.db.models import Avg
from rest_framework import filters, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .filters import TitleFilter
from .models import Category, Genre, Title
from .permissions import IsGetOrIsAdmin, IsOwnerOrModeratorOrAdmin
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    """The class returns all reviews of the titles, creates a new review."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrModeratorOrAdmin)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """The function returns a queryset filtered by the title id
        from the URL."""
        title = self.get_title()
        return title.reviews.all()

    def get_title(self):
        """The function returns the title whose id is obtained from the URL."""
        title_id = self.kwargs["title_id"]
        return get_object_or_404(Title, id=title_id)

    def perform_create(self, serializer):
        """The function adds the current user as review fields
        when creating it."""
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """The class returns all comments to a review, or creates a comment on a
    review, or modifies a comment."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrModeratorOrAdmin)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """The function returns a queryset filtered by the title id and review id
        from the URL."""
        review = self.get_review()
        return review.comments.all()

    def get_title(self):
        """The function returns the title whose id is obtained from the URL."""
        title_id = self.kwargs["title_id"]
        return get_object_or_404(Title, id=title_id)

    def get_review(self):
        """The function returns the review whose id is obtained
        from the URL."""
        title = self.get_title()
        reviews = title.reviews.all()
        review_id = self.kwargs["review_id"]
        return get_object_or_404(reviews, id=review_id)

    def perform_create(self, serializer):
        """The function adds the current user as comment fields
        when creating it."""
        serializer.save(author=self.request.user, review=self.get_review())


class CategoryViewSet(viewsets.ModelViewSet):
    """The class returns all categories. Name filtering available"""

    model = Category
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = (IsGetOrIsAdmin,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ("name",)
    lookup_field = "slug"
    http_method_names = [
        "get",
        "post",
        "delete",
    ]


class GenreViewSet(viewsets.ModelViewSet):
    """The class returns all genres. Name filtering available"""

    model = Genre
    queryset = Genre.objects.all().order_by("name")
    serializer_class = GenreSerializer
    permission_classes = (IsGetOrIsAdmin,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ("name",)
    lookup_field = "slug"
    http_method_names = [
        "get",
        "post",
        "delete",
    ]


class TitleViewSet(viewsets.ModelViewSet):
    """The class returns all titles.
    Filters available: category, genre, name, year
    """

    model = Title
    queryset = Title.objects.annotate(rating=Avg("reviews__score")).order_by(
        "rating"
    )
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsGetOrIsAdmin,
    )
    pagination_class = PageNumberPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
    ]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return TitleReadSerializer
        return TitleWriteSerializer
