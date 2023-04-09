from django.db import models
from LoginReg.models import User
from djmoney.models.fields import MoneyField
import datetime
from django.core.validators import MinValueValidator
# Create your models here.

class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    bio = models.CharField(blank=True,null=True,max_length=120, help_text='Enter company bio')

    def __str__(self):
        return self.user.username


class Notifications(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    topic=models.CharField(max_length=20,help_text='Topic',blank=True,null=True)
    content=models.CharField(max_length=200,help_text='Content',blank=True,null=True)
    def __str__(self):
        return self.topic
    


class Donation(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    grains=models.CharField(max_length=50,help_text='Grains',blank=True,null=True)
    cooked_food=models.CharField(max_length=50,help_text='Cooked_food',blank=True,null=True)
    quantity=models.IntegerField(help_text='No. Of People It Can Feed',validators=[MinValueValidator(1)])
    date_time=models.DateTimeField(default=datetime.datetime.now)
    ngo=models.CharField(max_length=30)
    profile_pic = models.ImageField(null=True, verbose_name="Profile Photo", upload_to = 'Profile-Pic/',help_text='Upload your Profile Photo',blank=True)


    def __str__(self):
        return self.user.username

class Volunteer(models.Model):
    First_name = models.CharField(max_length=20, help_text='Enter your First name')
    Last_name = models.CharField(max_length=20, help_text='Enter your Last name')
    phone = models.CharField(max_length=10,blank=True,null=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        help_text='Enter your Email',
        blank=True,null=True
    )
    address=models.CharField(max_length=100,blank=True,null=True)
    typeofwork=models.CharField(max_length=20,blank=True,null=True)
    ngo=models.CharField(max_length=30)
    why=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.First_name

class Community(models.Model):
    username = models.CharField(max_length=20,unique=True)
    caption=models.CharField(max_length=200,help_text='Caption',blank=True,null=True)
    profile_pic = models.ImageField(null=True, verbose_name="Community Photo", upload_to = 'Post/',help_text='Upload your Profile Photo',blank=True)

    def __str__(self):
        return self.username
    
class ContactUs(models.Model):
    name=models.CharField(max_length=20,blank=True,null=True)
    email=models.EmailField(max_length=100)
    phone = models.CharField(max_length=10,blank=True) 
    message=models.TextField(max_length=100,blank=True,null=True)


