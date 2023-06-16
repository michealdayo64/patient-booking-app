from django.contrib import admin
from .models import Ailments, Appointment, WriteUs, Payment
# Register your models here.
admin.site.register([Ailments, Appointment, WriteUs, Payment])
