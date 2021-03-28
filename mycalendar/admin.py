from django.contrib import admin
from mycalendar.models import Calendar, Event
# Register your models here.
admin.site.register(Calendar)
admin.site.register(Event)