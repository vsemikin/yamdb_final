from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for the Review model."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review
        read_only_fields = ("title",)

    def validate(self, data):
        """The function checks whether the review exists or not."""
        user = self.context["request"].user
        title_id = self.context["view"].kwargs.get("title_id")
        if (self.context["request"].method == "POST") and (
            Review.objects.filter(title_id=title_id, author=user).exists()
        ):
            raise serializers.ValidationError("Ошибка: Отзыв уже существует")
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comments model."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment
        read_only_fields = ("review",)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Categories model."""

    class Meta:
        exclude = ("id",)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for the Genres model."""

    class Meta:
        exclude = ("id",)
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    """Serializer for reading Titles model."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        required=True,
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        required=True,
        many=True,
    )

    class Meta:
        fields = "__all__"
        model = Title
