from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class UserForm(UserCreationForm):
    nickname = forms.CharField(label="별명")

    class Meta:
        model = get_user_model()
        fields = ("username", "nickname", "password1", "password2")

# model = User
# 커스터마이징해서 User 가 아닌 직접 get_user_model 로 설정해야함