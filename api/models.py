from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    """The model describes categories of titles (Music, Book, Film etc.)"""

    name = models.CharField(max_length=255, verbose_name="Категория")
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=False,
        verbose_name="Категория slug",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """The model describes Title genres. One title can have multiple genres"""

    name = models.CharField(max_length=255, verbose_name="Жанр")
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=False,
        verbose_name="Жанр slug",
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    """The model describes Titles for reviews by users"""

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="category_title",
        verbose_name="Категория",
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="genre_title",
        verbose_name="Жанр",
    )
    name = models.CharField(max_length=255, verbose_name="Название")
    year = models.PositiveSmallIntegerField(validators=[validate_year])
    description = models.TextField(
        max_length=1500,
        blank=True,
        verbose_name="Описание",
    )

    class Meta:
        verbose_name = "Название произведения"
        verbose_name_plural = "Названия произведений"


class Review(models.Model):
    """The model describes the reviews of the titles."""

    title = models.ForeignKey(
        "Title",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    text = models.TextField("Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviewers",
        verbose_name="Автор",
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(limit_value=1, message="Оценка меньше 1"),
            MaxValueValidator(limit_value=10, message="Оценка больше 10"),
        ],
        verbose_name="Оценка",
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text[:100]


class Comment(models.Model):
    """Review comments model."""

    review = models.ForeignKey(
        "Review",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
    )
    text = models.TextField("Комментарий")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-id"]

    def __str__(self):
        return self.text[:50]
