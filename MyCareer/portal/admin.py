from django.contrib import admin
from .models import Profile, Job, Application

# Register your models here.

admin.site.register(Profile)
admin.site.register(Job)
admin.site.register(Application)