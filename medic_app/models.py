from django.db import models
from auths.models import Account, AdditionalInformation
# Create your models here.


class WriteUs(models.Model):
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_no = models.CharField(max_length=50, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.email


class Ailments(models.Model):
    user = models.ForeignKey(Account, default=False,
                             on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image_icon = models.ImageField(upload_to='picture', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Appointment(models.Model):
    add_info = models.ForeignKey(
        AdditionalInformation, default=False, on_delete=models.CASCADE, null=True, blank=True)
    ailment_id = models.ForeignKey(
        Ailments, null=True, blank=True, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=30, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    is_booked = models.BooleanField(default=False)
    date = models.DateField()
    appointment_time = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.add_info}'


class Payment(models.Model):
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, blank=True)
    app_id = models.ForeignKey(
        Appointment, null=True, blank=True, on_delete=models.CASCADE)
    is_payed = models.BooleanField(default=False)
    payment_prove = models.ImageField(upload_to='media', null=True, blank=True)
    payment_IDnumber = models.CharField(null=True, blank=True, max_length=70)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
