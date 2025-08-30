from django.forms import ModelForm
from django.contrib.auth.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        error_messages = {
            "username": {"required": "ユーザー名は必須です"},
            "password": {"required": "パスワードは必須です"},
        }
