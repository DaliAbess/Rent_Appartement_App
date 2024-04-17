from django.db import models
from django.contrib.auth.models import AbstractUser

from model_utils import Choices

# Create your models here.

class User(AbstractUser):
    username=models.CharField(max_length=20,unique=False,default="user")#abess
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(unique=True,max_length=255)
    password = models.CharField(unique=False,null=True,max_length=255)
    phone = models.CharField(unique=True,null=True,blank=True,max_length=255)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    STATUS = Choices('active','suspended','disabled')
    status = models.CharField(choices=STATUS,null=False,default=STATUS.active,max_length=255)
    ROLE = Choices('admin','user','owner')
    role = models.CharField(choices=ROLE,default=ROLE.admin,max_length=255)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'Users'

    # Setting username by default equal to email
    USERNAME_FIELD = 'email'
    # Setting Required Field for User
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'phone',
        ]
objects = User()
