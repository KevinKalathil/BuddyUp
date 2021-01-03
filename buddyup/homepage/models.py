from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     route = models.CharField(max_length=256, blank=True, null=True)
#
#     def __str__(self):
#         return self.user.username

#
#
# class MyUserManager(BaseUserManager):
#     def create_user(self, email, username, password=None):
#         if not email:
#             raise ValueError("USER MUST HAVE AN EMAIL ADDRESS")
#         if not username:
#             raise ValueError("USER MUST HAVE A USERNAME")
#         user = self.model(
#             email = self.normalize_email(email),
#             username = username
#         )
#
#         user.set_password(password)
#         user.save(user.self_db)
#         return user
#
#     def super_create_user(self, email, username, password):
#         user = self.model(
#             email = self.normalize_email(email),
#             password = password,
#             username = username
#         )
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(user.self_db)
#
# # Create your models here.
# class UserModel(AbstractBaseUser):
#     username = models.TextField(max_length=30, unique=True)
#     email = models.EmailField(verbose_name="email", max_length=60, unique=True)
#     date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
#     last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
#     is_admin = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#
#     route = models.TextField(max_length=300)
#
#     USERNAME_FIELD='email'
#     REQUIRED_FIELDS = ['username']
#
#     objects = MyUserManager()
#
#     def __str__(self):
#         return self.email
#
#     def has_perm(self, perm, obj=None):
#         return self.is_admin
#
#     def has_module_perms(self, app_label):
#         return True
#
#
