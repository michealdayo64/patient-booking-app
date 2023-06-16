from django import forms
from .models import WriteUs


class WriteUsForm(forms.ModelForm):
    class Meta:
        model = WriteUs
        fields = "__all__"

