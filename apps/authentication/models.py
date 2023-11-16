# Create your models here.
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/<username>/<filename>
    return "users/{0}/{1}".format(instance.first_name, filename)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, null=True, unique=True)
    supplier_name = models.CharField(max_length=255, unique=True)
    manufacturer_number = models.TextField(null=True, blank=True)
    vendor_number = models.TextField(null=True, blank=True)
    classic_industries = models.BooleanField(default=False)
    last_p_n = models.TextField(null=True, blank=True)
    atech = models.BooleanField(default=False)
    npw = models.BooleanField(default=False)
    jegs = models.BooleanField(default=False)
    speedway = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    relationship_status = models.TextField(null=True, blank=True)
    initial = models.TextField(null=True, blank=True)
    supplier = models.TextField(null=True, blank=True)
    website = models.TextField(null=True, blank=True)
    account_numbers = models.TextField(null=True, blank=True)
    log_on_info = models.TextField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)
    user_address = models.TextField(null=True, blank=True)
    city_state_zip_code = models.TextField(null=True, blank=True)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    contact_email = models.EmailField(max_length=255)
    contact_phone = models.TextField(null=True, blank=True)

    is_verified = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to=user_directory_path,
                                        blank=True, verbose_name='Profile Picture')

    gender = models.CharField(max_length=1, choices=(
        ("m", "Male"),
        ("f", "Female"),
        ("0", "Other"),
    ), blank=True)

    about = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    auth_provider = models.CharField(max_length=255, blank=False, null=False,
                                     default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    # def __unicode__(self):
    #     return self.profile_picture

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def __str__(self):
        return "{} - {} - {} - {}".format(self.username,
                                          self.email,
                                          self.created_at,
                                          self.updated_at)
