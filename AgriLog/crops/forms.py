from django import forms

from .models import Field


class FieldNotesForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ["notes"]


class FieldRenameForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get("name")

        if (
            Field.objects.filter(owner=self.user, name__iexact=name)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("Masz już pole o takiej nazwie!")

        return name
