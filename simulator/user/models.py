import imp
from operator import mod
from queue import Empty
from time import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from django.core.validators import RegexValidator
# Create your models here.


class CustomUserManager(BaseUserManager):

    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,null=False,blank=False)
    #region = models.CharField(unique=True,null=False,blank=False,max_length=3)
    #phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    #phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False,null=False) 
    is_active = models.BooleanField(default = True)
    date_joined = models.DateTimeField(default=timezone.now,null=False,blank=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
  #  REQUIRED_FIELDS = ['region','phone_number']
    REQUIRED_FIELDS: []
    objects = CustomUserManager()

    def has_module_perms(self, app_label):
        return True

    def __str__(self) -> str:
        return self.email

