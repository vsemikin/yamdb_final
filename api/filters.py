import django_filters

from .models import Title


class TitleFilter(django_filters.FilterSet):
    category = django_filters.filters.CharFilter(
        field_name="category__slug",
        lookup_expr="contains",
    )
    genre = django_filters.filters.CharFilter(
        field_name="genre__slug",
        lookup_expr="contains",
    )
    name = django_filters.filters.CharFilter(
        field_name="name",
        lookup_expr="contains",
    )
    year = django_filters.filters.NumberFilter(
        field_name="year",
        lookup_expr="iexact",
    )

    class Meta:
        model = Title
        fields = [
            "category",
            "genre",
            "name",
            "year",
        ]
