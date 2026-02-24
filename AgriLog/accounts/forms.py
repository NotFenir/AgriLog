from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class EmailRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["email"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        user.username = self.cleaned_data["email"]
        if commit:
            user.save()

        return user
