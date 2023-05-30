from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView, Request, Response, status
from _kenzie_buster.pagination import CustomPageNumberPagination
from .serializers import MovieSerializer, MovieOrderSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsEmployeeOrReadOnly2
from django.shortcuts import get_object_or_404
from .models import Movie


class MovieView(APIView, CustomPageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly2]

    def post(self, req: Request) -> Response:
        movie = MovieSerializer(data=req.data)
        movie.is_valid(raise_exception=True)
        movie.save(user=req.user)
        return Response(movie.data, status.HTTP_201_CREATED)

    def get(self, req: Request) -> Response:
        movies = Movie.objects.all()
        result_page = self.paginate_queryset(movies, req, view=self)
        movies = MovieSerializer(result_page, many=True)
        return self.get_paginated_response(data=movies.data)


class MovieDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly2]

    def get(self, _: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        movie = MovieSerializer(movie)
        return Response(data=movie.data)

    def delete(self, _: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, req: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        mo = MovieOrderSerializer(data=req.data)
        mo.is_valid(raise_exception=True)
        mo.save(order=req.user, movie_id=movie.id)
        return Response(mo.data, status.HTTP_201_CREATED)
