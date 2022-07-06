from django import forms
from .models import Signup
from django.utils.translation import ugettext as _


class EmailSignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "type": "email",
        "name": "email",
        "id": "email",
        "placeholder": _("Type your email address"),
    }), label="")

    class Meta:
        model = Signup
        fields = ('email', )
