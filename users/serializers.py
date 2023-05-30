from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from rest_framework.serializers import (
    Serializer, IntegerField, CharField, DateField,
    BooleanField, SerializerMethodField, EmailField)


class CustomJWTSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["is_superuser"] = user.is_superuser
        return token


class UserSerializer(Serializer):
    id = IntegerField(read_only=True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    birthdate = DateField(allow_null=True, default=None)
    password = CharField(max_length=127, write_only=True)
    is_employee = BooleanField(default=False)
    is_superuser = SerializerMethodField()

    username = CharField(
        max_length=50,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="username already taken."
        )]
    )

    email = EmailField(
        max_length=127,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="email already registered.",
        )]
    )

    def get_is_superuser(self, obj: User) -> bool:
        return obj.is_employee

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)

    def update(self, inst: User, valid_dt: dict) -> User:
        for key, value in valid_dt.items():
            setattr(inst, key, value)
        inst.save()
        return inst
