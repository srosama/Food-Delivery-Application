from typing import Any, Optional
from django.db import models
from django.contrib.auth.models import UserManager, PermissionsMixin, AbstractBaseUser, AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django_countries.fields import CountryField
import uuid
import pathlib
from django.db.models.signals import post_save

#Build a customer > phone, full-name, img

class CustomUserManger(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not pro")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)   
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    fullName = models.CharField(max_length=255, blank=True, default='')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login  = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManger()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'

    def get_full_name(self):
        return self.fullName
    
    def get_short_name(self):
        return self.fullName or self.email.split('@')[0]




#Account
class customerAccountDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20, null=True)
    # image = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.user.fullName

# class customerAddress(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    country = CountryField(blank=True, default='Saudi') 
#    city = models.CharField(max_length=200, default='Riyadh', null=True)
#    Address_line_1 = models.CharField(max_length=500, null=True)
#    Address_line_2 = models.CharField(max_length=500)
    

# class customerPayment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     card_number = models.IntegerField(null=True, )
#     expiration_date = models.DateField()
#     cvc = models.CharField(max_length=4)
#     cardholder = models.CharField(max_length=40)



def image_upload_to(instance, filename):
    fpath = pathlib.Path(settings.MEDIA_ROOT)
    new_fname = str(uuid.uuid1())
    return f""

#Restaurants Owners
class AddNewRestaurantV2(models.Model):
    id_Restaurant = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    logo = models.ImageField(blank=True)
    bannar_img = models.ImageField(blank=True)

    description = models.TextField()
    time_for_delivery = models.PositiveIntegerField()
    price_Max = models.DecimalField(max_digits=8, decimal_places=2)
    price_Min = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    

class testImg(models.Model):
    name = models.CharField(max_length=100)
    testImg = models.ImageField(blank=True)


# def create_restaurant(sender, instance, created, **kwargs):
#     if created:
#         restaurant = AddNewRestaurantV2(user=instance)
#         restaurant.save()

# post_save.connect(create_restaurant, sender=User)