from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class AppUser(AbstractUser):
    first_name = models.CharField(max_length=100,blank=True,null=True)
    last_name = models.CharField(max_length=100,blank=True,null=True)
    is_admin = models.BooleanField(default=False)
    date_of_birth = models.CharField(max_length = 100,blank=True,null=True)
    photo_url = models.CharField(max_length = 100,blank=True,null=True)
    email = models.EmailField( blank=True, null=True)
    