from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from homepage.models import UserModel
# from homepage.models import UserProfile


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']

class LoginUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1']