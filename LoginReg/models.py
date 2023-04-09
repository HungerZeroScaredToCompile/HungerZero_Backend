from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager

# Create your models here.
class User(AbstractBaseUser):
    username = models.CharField(max_length=20,unique=True, help_text='Enter your Username')
    First_name = models.CharField(max_length=20, help_text='Enter your First name')
    Last_name = models.CharField(max_length=20, help_text='Enter your Last name')
    phone = models.CharField(max_length=10,blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        help_text='Enter your Email',
        blank=True
    )
    address=models.CharField(max_length=100,blank=True)
    profile_pic = models.ImageField(null=True, verbose_name="Profile Photo", upload_to = 'Profile-Pic/',help_text='Upload your Profile Photo',blank=True)
    # email_token =  models.CharField(max_length=250, null=True, blank=True)
    # password_reset_token = models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_donor=models.BooleanField(default=True)
    is_NGO=models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','First_name','Last_name']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    def is_verified(self):
        return (self.is_email_verified)
