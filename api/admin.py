from django.contrib import admin

from .models import CustomUser, Global, Spam

admin.site.register(CustomUser)
admin.site.register(Global)
admin.site.register(Spam)