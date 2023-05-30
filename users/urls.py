from django.urls import path
from .views import UserView, LoginJWTView, UserDeatilsView


urlpatterns = [
    path("users/", view=UserView.as_view()),
    path("users/<int:user_id>/", view=UserDeatilsView.as_view()),
    path("users/login/", view=LoginJWTView.as_view())
]
