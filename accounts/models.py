from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django_resized import ResizedImageField

class MyAccountManager(BaseUserManager):
    def create_user(self, full_name, username, email, phone_number, password):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            full_name=full_name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, username, password, full_name, phone_number):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            full_name=full_name,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    full_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    profileImage = ResizedImageField(size=[100, 180],quality=100, upload_to='profile_pic', default=None, blank=True, null=True)
    # add another fields here if required

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_verified_artist = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'phone_number']

    objects = MyAccountManager()

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
