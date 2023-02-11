from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from reviews.models import (Category, Comment,  # isort:skip
                            Genre, Review, Title)

User = get_user_model()


class NameSlugSerializer(serializers.ModelSerializer):

    class Meta:
        lookup_field = "slug"
        exclude = ("id",)


class CategorySerializer(NameSlugSerializer):

    class Meta(NameSlugSerializer.Meta):
        model = Category


class GenreSerializer(NameSlugSerializer):

    class Meta(NameSlugSerializer.Meta):
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """
    Designated for title instance creation or update.
    """
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        many=True,
    )
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description",
                  "genre", "category",)

    def validate_year(self, value):
        if value > timezone.now().year:
            raise serializers.ValidationError(
                "Год выпуска не может быть больше текущего!"
            )
        return value

    def validate(self, validated_data):
        request = self.context.get("request")
        if request and request.method == "POST":
            if Title.objects.filter(
                name=validated_data.get("name"),
                category=validated_data.get("category")
            ).exists():
                raise serializers.ValidationError("Title already exists.")
        return validated_data


class TitleReadOnlySerializer(serializers.ModelSerializer):
    """
    Designated for title instance listing or retrieving.
    """
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description",
                  "genre", "category", "rating",)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )
    score = serializers.IntegerField(
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        )
    )

    class Meta:
        model = Review
        fields = ("id", "author", "text", "score", "pub_date")

    def validate(self, validated_data):
        request = self.context.get("request")
        if request and request.method == "POST":
            title_id = self.context["view"].kwargs.get("title_id")
            title = get_object_or_404(Title, pk=title_id)
            if title.reviews.filter(  # type:ignore
                author=request.user
            ).exists():
                raise serializers.ValidationError(
                    "Можно оставить только один отзыв на произведение"
                )
        return validated_data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
