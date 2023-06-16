from django.db import models

# Create your models here.

def get_profile_image_filepath(self, filename):
    return f'review_images/{self.pk}/{"profile_image.png"}'


def get_default_profile_image():
    return "picture/dummy_image.png"


class Review(models.Model):
    firstname = models.CharField(max_length = 50, null = True, blank = True)
    lastname = models.CharField(max_length = 50, null = True, blank = True)
    treated_on = models.CharField(max_length = 50, null = True, blank = True)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath,
                                      null=True, blank=True, default=get_default_profile_image)
    comments = models.TextField(null = True, blank = True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.firstname
