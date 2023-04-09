from django.contrib import admin
from .models import Volunteer,Notifications,Profile,Donation,Community

# Register your models here.
admin.site.register(Volunteer)
admin.site.register(Notifications)
admin.site.register(Profile)
admin.site.register(Donation)
admin.site.register(Community)
