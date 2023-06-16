from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from auths.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2', )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(
                pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(
                pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(
            'Username "%s" is already in use.' % account)


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("email", "password", )

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError(
                    "Invalid Login. Enter a correct email or password")
            if not user.is_active:
                raise forms.ValidationError("You need to verify your email")


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ("first_name", "middle_name", "last_name",
                  "phone_number", "address",)


REACH_YOU = (
    ('EMAIL', 'EMAIL'),
    ('PHONE', 'PHONE'),
)

BEST_TIME_REACH_YOU = (
    ('MORNING', 'MORNING'),
    ('AFTERNOON', 'AFTERNOON'),
    ('EVENING', 'EVENING'),
)

INSURANCE_OR_PAY = (
    ('INSURANCE', 'INSURANCE'),
    ('PAY', 'PAY'),
)

GENDER = (
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE'),
    ('NO', 'NO')
)

SECONDARY_INSURANCE = (
    ('YES', 'YES'),
    ('NO', 'NO'),
)

CURRENT_SUBSCRIBER = (
    ('YES', 'YES'),
    ('NO', 'NO')
)


class AdditionalInformationForm(forms.Form):
    firstname = forms.CharField(widget=forms.TextInput)
    lastname = forms.CharField(widget=forms.TextInput)
    email = forms.EmailField(max_length=200)
    phone_number = forms.CharField(widget=forms.TextInput, required=False)
    dob = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter date of birth'
    }))
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDER)
    city = forms.CharField(widget=forms.TextInput, required=False)
    state = forms.CharField(widget=forms.TextInput, required=False)
    zipCode = forms.CharField(widget=forms.TextInput, required=False)
    best_way_reach = forms.ChoiceField(
        widget=forms.RadioSelect, choices=REACH_YOU)
    best_time_reach = forms.ChoiceField(
        widget=forms.RadioSelect, choices=BEST_TIME_REACH_YOU)
    insurance_or_pay = forms.ChoiceField(
        widget=forms.RadioSelect, choices=INSURANCE_OR_PAY)
    my_insure_carrier = forms.CharField(
        widget=forms.TextInput, required=False)
    insurance = forms.CharField(widget=forms.TextInput, required=False)
    do_you_have_secondary_insurance = forms.ChoiceField(
        widget=forms.RadioSelect, choices=SECONDARY_INSURANCE)
    secondary_insurance_carrier = forms.CharField(
        widget=forms.TextInput, required=False)
    secondary_insurance = forms.CharField(
        widget=forms.TextInput, required=False)
    current_psychiatric_diagnosis = forms.CharField(
        widget=forms.TextInput, required=False)
    current_medications = forms.CharField(
        widget=forms.TextInput, required=False)
    current_psychiatric_prescriber = forms.ChoiceField(
        widget=forms.RadioSelect, choices=CURRENT_SUBSCRIBER)
    history_of_suicide_attempts = forms.CharField(
        widget=forms.TextInput, required=False)
    history_of_self_injurious_behavior = forms.CharField(
        widget=forms.TextInput, required=False)
    history_of_eating_disorder = forms.CharField(
        widget=forms.TextInput, required=False)
    history_of_substance_abuse = forms.CharField(
        widget=forms.TextInput, required=False)
    emergency_contact_firstname = forms.CharField(
        widget=forms.TextInput, required=False)
    emergency_contact_phone = forms.CharField(
        widget=forms.TextInput, required=False)
    referred_by = forms.CharField(widget=forms.TextInput, required=False)
    additional_comments = forms.CharField(
        widget=forms.TextInput, required=False)
