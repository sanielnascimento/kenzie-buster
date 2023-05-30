from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CharField, EmailField, DateField, BooleanField)


class User(AbstractUser):
    username = CharField(max_length=150, unique=True)
    email = EmailField(max_length=127, unique=True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    birthdate = DateField(null=True)
    password = CharField(max_length=127)
    is_employee = BooleanField(null=True, default=False)

    def __repr__(self) -> str:
        return f"< User: {self.id} = {self.first_name} >"
