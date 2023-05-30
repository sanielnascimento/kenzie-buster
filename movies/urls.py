from django.urls import path
from .views import MovieView, MovieDetailsView, MovieOrderView


urlpatterns = [
    path("movies/", view=MovieView.as_view()),
    path("movies/<int:movie_id>/", view=MovieDetailsView.as_view()),
    path("movies/<int:movie_id>/orders/", view=MovieOrderView.as_view())
]
