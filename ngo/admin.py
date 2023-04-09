from django.contrib import admin
from .models import Profile,Stats,Feedback
# Register your models here.

admin.site.register(Profile)
#admin.site.register(Stats)
#admin.site.register(Feedback)

@admin.register(Stats)
class StatsAdmin(admin.ModelAdmin):
    list_display = ['name','no_of_volunteers','no_of_donations','no_of_ppl_helped']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name','ratings','description']

