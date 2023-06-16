from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/{"profile_image.png"}'


def get_default_profile_image():
    return "picture/dummy_image.png"


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    fifteen_min_trial = models.BooleanField(
        default=False, null=True, blank=True)
    profile_updated = models.BooleanField(default=False, null=True, blank=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath,
                                      null=True, blank=True, default=get_default_profile_image)
    hide_email = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


class AdditionalInformation(models.Model):
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(
        verbose_name="email", max_length=60, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    fifteen_min_trial = models.BooleanField(
        default=False, null=True, blank=True)
    dob = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zipCode = models.CharField(max_length=50, null=True, blank=True)
    best_way_reach = models.CharField(
        max_length=20, null=True, blank=True)
    best_time_reach = models.CharField(
        max_length=20, null=True, blank=True)
    insurance_or_pay = models.CharField(
        max_length=20, null=True, blank=True)
    insurance = models.CharField(
        max_length=20, null=True, blank=True)
    my_insure_carrier = models.CharField(
        max_length=20, null=True, blank=True)
    do_you_have_secondary_insurance = models.CharField(
        max_length=20, null=True, blank=True)
    secondary_insurance_carrier = models.CharField(
        max_length=20, null=True, blank=True)
    secondary_insurance = models.CharField(
        max_length=20, null=True, blank=True)
    current_psychiatric_diagnosis = models.CharField(
        max_length=20, null=True, blank=True)
    current_medications = models.CharField(
        max_length=20, null=True, blank=True)
    current_psychiatric_prescriber = models.CharField(
        max_length=20, null=True, blank=True)
    history_of_suicide_attempts = models.TextField(
        null=True, blank=True)
    history_of_self_injurious_behavior = models.TextField(
        null=True, blank=True)
    history_of_eating_disorder = models.TextField(
        null=True, blank=True)
    history_of_substance_abuse = models.TextField(
        null=True, blank=True)
    emergency_contact_firstname = models.CharField(
        max_length=20, null=True, blank=True)
    emergency_contact_phone = models.CharField(
        max_length=20, null=True, blank=True)
    referred_by = models.CharField(
        max_length=20, null=True, blank=True)
    additional_comments = models.TextField(
        null=True, blank=True)

    def __str__(self):
        return self.firstname
