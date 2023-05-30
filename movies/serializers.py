from .models import Movie, Ratings, MovieOrder
from rest_framework.serializers import (
    Serializer, IntegerField, CharField, DecimalField,
    DateTimeField, ChoiceField, EmailField)


class MovieSerializer(Serializer):
    id = IntegerField(read_only=True)
    title = CharField(max_length=127)
    synopsis = CharField(allow_null=True, default=None)
    added_by = EmailField(source="user.email", read_only=True)
    duration = CharField(
        max_length=127, allow_null=True, default=None)

    rating = ChoiceField(
        allow_null=True,
        choices=Ratings.choices,
        default=Ratings.G)

    def create(self, validated_data: dict) -> Movie:
        return Movie.objects.create(**validated_data)


class MovieOrderSerializer(Serializer):
    id = IntegerField(read_only=True)
    title = CharField(
        source="movie.title", read_only=True)
    price = DecimalField(max_digits=8, decimal_places=2)
    buyed_by = CharField(source="order.email", read_only=True)
    buyed_at = DateTimeField(read_only=True)

    def create(self, validated_data: dict) -> Movie:
        return MovieOrder.objects.create(**validated_data)
