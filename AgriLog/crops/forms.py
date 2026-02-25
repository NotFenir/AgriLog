from django import forms

from .models import CropType, Cultivation, Field, Treatment


class FieldNotesForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ["notes"]


class FieldEditForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ["name", "area_size", "soil_class"]
        # Możemy zdefiniować widgety tutaj, by wymusić klasy CSS
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "area_size": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "soil_class": forms.Select(
                attrs={"class": "form-select"}
            ),  # Select dla klasy ziemi
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)


class TreatmentAddForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ["treatment_type", "date", "crop_type", "description"]
        widgets = {
            "treatment_type": forms.Select(
                attrs={"class": "form-select rounded-3", "id": "id_treatment_type"}
            ),
            "date": forms.DateInput(
                attrs={"class": "form-control rounded-3", "type": "date"}
            ),
            "crop_type": forms.Select(attrs={"class": "form-select rounded-3"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control rounded-3",
                    "rows": 3,
                    "placeholder": "Opisz szczegóły zabiegu...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcjonalnie: możesz tu przefiltrować CropType, jeśli chcesz
        self.fields["crop_type"].queryset = CropType.objects.all()
        self.fields["crop_type"].empty_label = "Wybierz roślinę (tylko dla siewu)"


class CultivationEditForm(forms.ModelForm):
    class Meta:
        model = Cultivation
        fields = ["status", "sowing_date", "yield_amount"]

        widgets = {
            "sowing_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control rounded-3"}
            ),
            "status": forms.Select(attrs={"class": "form-select rounded-3"}),
            "yield_amount": forms.NumberInput(
                attrs={"class": "form-control rounded-3", "step": "0.01"}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)


class CultivationNotesForm(forms.ModelForm):
    class Meta:
        model = Cultivation
        fields = ["notes"]
