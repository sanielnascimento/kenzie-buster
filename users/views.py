from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, CustomJWTSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from .permissions import IsAccountOwner
from .models import User


class LoginJWTView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer


class UserView(APIView):
    def post(self, req: Request) -> Response:
        user = UserSerializer(data=req.data)
        if user.is_valid():
            user.save()
            return Response(user.data, status=status.HTTP_201_CREATED)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, _: Request) -> Response:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDeatilsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def patch(self, req: Request, user_id: int) -> Response:
        gotten = get_object_or_404(User, id=user_id)
        self.check_object_permissions(req, gotten)
        user = UserSerializer(
            instance=gotten, data=req.data, partial=True)
        if user.is_valid():
            if user.validated_data["password"]:
                user.validated_data["password"] = make_password(
                        user.validated_data["password"])
            user.save()
            return Response(user.data, status=status.HTTP_200_OK)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, req: Request, user_id: int) -> Response:
        gotten = get_object_or_404(User, id=user_id)
        self.check_object_permissions(req, gotten)
        serializer = UserSerializer(gotten)
        return Response(serializer.data)
