from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_title_year

User = get_user_model()


class Category(models.Model):
    """Категории (типы) произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name="name",
        help_text="Category name"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="slug",
        help_text="Category slug"
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Категории жанров."""
    name = models.CharField(
        max_length=256,
        verbose_name="genre",
        help_text="Genre name"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="slug",
        help_text="Genre slug"
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы (определённый фильм, книга или песня).
    """
    name = models.CharField(
        max_length=256,
        verbose_name="name",
        help_text="Title name"
    )
    year = models.PositiveSmallIntegerField(
        validators=[validate_title_year],
        verbose_name="year",
        help_text="Title publish year"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="category",
        help_text="Title category"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="description",
        help_text="Title description"
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="genre",
        help_text="Title genre set"
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        constraints = [
            models.UniqueConstraint(
                fields=("name", "category"),
                name="unique_title_name_category"
            ),
        ]

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзывы."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="author",
        related_name="reviews",
        help_text="Review's author"
    )
    text = models.TextField(
        verbose_name="text",
        help_text="Review's text"
    )
    title = models.ForeignKey(
        Title,
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name="title",
        help_text="Title of review's subject"
    )
    pub_date = models.DateTimeField(
        verbose_name="pub_date",
        auto_now_add=True,
        db_index=True,
        help_text="Publication date"
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, "Score can not be less than one."),
            MaxValueValidator(10, "Score can not be more than ten.")
        ],
        verbose_name="score",
        help_text="Review's title score"
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"],
                name="only_one_review"
            ),
        ]

    def __str__(self):
        return self.title.name


class Comment(models.Model):
    """Комментарии к отзывам."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="author",
        help_text="Comment's author"
    )
    text = models.TextField(
        verbose_name="text",
        help_text="Text of comment"
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="review",
        help_text="Review that is comment's subject"
    )
    pub_date = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name="pub_date",
        help_text="Date of comment publication"
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"{self.review}"
