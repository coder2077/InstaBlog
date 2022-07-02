from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm):
		model = CustomUser
		fields = ('first_name', 'username', 'email',)


class CustomUserChangeForm(UserChangeForm):
	class Meta:
		model = CustomUser
		fields = ('profile_pic', 'first_name', 'bio', 'email',)

