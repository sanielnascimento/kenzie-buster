from django.db.models import (
    TextChoices, Model, CharField, ForeignKey, ManyToManyField,
    TextField, CASCADE, DateTimeField, DecimalField)


class Ratings(TextChoices):
    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"


class Movie(Model):
    class Meta:
        ordering = ["id"]

    title = CharField(max_length=127)
    duration = CharField(
        max_length=10, null=True, default=None)
    rating = CharField(
        max_length=20, null=True, choices=Ratings.choices,
        default=Ratings.G)
    synopsis = TextField(null=True, default=None)

    user = ForeignKey(
        "users.User", on_delete=CASCADE, related_name="movies")

    orders = ManyToManyField(
        "users.User", through="movies.MovieOrder",
        related_name="ordered_movies")

    def __repr__(self) -> str:
        return f"< Movie: {self.id} = {self.title} >"


class MovieOrder(Model):
    movie = ForeignKey("movies.Movie", on_delete=CASCADE,
                       related_name="movies_ordereds")

    order = ForeignKey("users.User", on_delete=CASCADE,
                       related_name="movie_orders")
    buyed_at = DateTimeField(auto_now_add=True)
    price = DecimalField(max_digits=8, decimal_places=2)

    def __repr__(self) -> str:
        return f"< MovieOrder: {self.id} = {self.movie.title} >"
