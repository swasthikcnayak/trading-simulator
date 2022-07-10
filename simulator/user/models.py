from distutils.command.upload import upload
from email.policy import default
from PIL import Image
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
    is_active = models.BooleanField(default = True)
    date_joined = models.DateTimeField(default=timezone.now,null=False,blank=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    
    objects = CustomUserManager()

    def has_module_perms(self, app_label):
        return True

    def __str__(self) -> str:
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.png',upload_to='profile_pics/%Y/%m/')
    first_name = models.CharField(max_length=50, default=None, blank=True, null=True)
    last_name = models.CharField(max_length=30, default=None, blank=True, null=True)
    wallet = models.BigIntegerField(default=100000)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        img_width, img_height = img.size

        output_size = (500, 500)
        box = ((img_width - min(img.size)) // 2, (img_height - min(img.size)) //
               2, (img_width + min(img.size)) // 2, (img_height + min(img.size)) // 2)
        img = img.crop(box)
        img.thumbnail(output_size)
        img.save(self.image.path)
