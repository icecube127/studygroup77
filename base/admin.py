from django.contrib import admin

# Register your models here.
from .models import Profile, Room, Topic, Message, Mathhistory

admin.site.register(Profile)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Mathhistory)