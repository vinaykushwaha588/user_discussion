import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.core.validators import validate_email
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models

name_validator = RegexValidator(r'^[a-zA-Z ]+$', 'Only alphabetic characters are allowed.')


## custom user manager


class UserManager(BaseUserManager):
    def create_user(self, email, password, mobile=None, name=None, **extra_fields):
        if not email:
            raise ValueError("Email id required!")

        email = self.normalize_email(email)
        user = self.model(email=email, mobile=mobile, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, mobile, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True!')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True!')

        return self.create_user(email, password, mobile, **extra_fields)


# Create your models here.

class UUIDBase(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True


# Create your models here.
class User(UUIDBase, AbstractBaseUser, PermissionsMixin):
    def validate_mobile(value):
        if len(value) != 10:
            raise ValidationError("Mobile number must be exactly 10 digits long.")

    name = models.CharField(max_length=100, null=True, validators=[name_validator])
    email = models.EmailField(unique=True, validators=[validate_email])
    mobile = models.CharField(unique=True, max_length=15, null=True, blank=True, validators=[validate_mobile])
    status = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile']
    objects = UserManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    

class Discussion(UUIDBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussion', null=True, blank=True)
    text = models.TextField()
    image = models.ImageField(upload_to='images/', null=True)
    hashtags = models.CharField(max_length=100, null=True)

    def __str__(self):
        return "{} - {}".format(self.user.name, self.text)
    