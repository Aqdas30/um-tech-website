from django.contrib import admin

# Register your models here.

from .models import Contact, Service

admin.site.register(Service)
admin.site.register(Contact)