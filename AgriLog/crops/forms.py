from django import forms

from .models import Field


class FieldNotesForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ["notes"]
