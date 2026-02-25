from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
import datetime
import uuid


class CropType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Field(models.Model):
    class SoilClass(models.TextChoices):
        I = "I", "I klasa"
        II = "II", "II klasa"
        III = "III", "III klasa"
        IV = "IV", "IV klasa"
        V = "V", "V klasa"
        VI = "VI", "VI klasa"

    name = models.CharField(max_length=100)
    area_size = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.TextField(verbose_name="Opis", blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="fields",
        blank=True,
        null=True,
    )
    soil_class = models.CharField(choices=SoilClass.choices, default=SoilClass.V)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("field_detail", kwargs={"pk": self.pk})

    def current_year(self):
        return (
            self.cultivations.order_by("-year").values_list("year", flat=True).first()
        )

    def clean(self):
        if Field.objects.filter(owner=self.owner, name__iexact=self.name).exists():
            raise ValidationError("Masz już pole o takiej nazwie!")

    def latest_cultivations(self):
        latest_year = self.current_year()
        return self.cultivations.filter(year=latest_year)


class Cultivation(models.Model):
    class Status(models.TextChoices):
        PROGRESS = "PG", "W trakcie"
        COMPLETED = "CP", "Zakończono (zebrano)"
        CANCELLED = "CL", "Anulowano (nie przetrwaly)"

    field = models.ForeignKey(
        Field, on_delete=models.SET_NULL, null=True, related_name="cultivations"
    )
    crop_type = models.ForeignKey(
        CropType, on_delete=models.SET_NULL, null=True, related_name="cultivations"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="cultivations",
        blank=True,
        null=True,
    )
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    notes = models.TextField(verbose_name="Opis", blank=True, null=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.PROGRESS
    )
    year = models.PositiveIntegerField()
    yield_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Plony (w kg)",
        blank=True,
        null=True,
        default=0,
    )
    sowing_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-year"]

    def __str__(self):
        return f"{self.field.name} - {self.crop_type.name} ({self.year})"

    def clean(self):
        current_year = timezone.now().year

        if self.year < 1970:
            raise ValidationError({"year": f"Rok {self.year} jest zbyt dawny"})

        if self.year > current_year + 10:
            raise ValidationError(
                {"year": f"Rok {self.year} jest zbyt odległy w przyszłości"}
            )

        if self.yield_amount < 0:
            raise ValidationError(
                {
                    "yield_amount": f"Nie można wpisać ujemną wartość zebranych plonów (podano: {self.yield_amount})"
                }
            )

    def save(self, *args, **kwargs):
        base_string = f"{self.year}-{self.field.name}-{self.crop_type.name}"
        new_slug = slugify(base_string)

        if Cultivation.objects.filter(slug=new_slug).exclude(pk=self.pk).exists():
            new_slug = f"{new_slug}-{str(uuid.uuid4())[:4]}"

        if not self.sowing_date and self.year:
            self.sowing_date = datetime.date(self.year, 9, 1)

        self.slug = new_slug
        super().save(*args, **kwargs)

    @property
    def is_active_now(self):
        return self.year == timezone.now().year


class Treatment(models.Model):
    class TreatmentType(models.TextChoices):
        SOWING = "SW", "Siew"
        FERTILIZING = "FT", "Nawożenie"
        LIMING = "LM", "Wapnowanie"
        PROTECTION = "PT", "Ochrona roślin"
        HARVEST = "HV", "Zbiór"
        PLOWING = "PL", "Orka"
        HARROWING = "HR", "Bronowanie"
        CULTIVING = "CT", "Gruberowanie"
        DISCING = "DC", "Talerzowanie"
        OTHER = "OT", "Inna czynność"

    field = models.ForeignKey(
        Field, on_delete=models.CASCADE, related_name="treatments", blank=True
    )
    treatment_type = models.CharField(
        max_length=2, choices=TreatmentType.choices, default=TreatmentType.OTHER
    )
    date = models.DateField(verbose_name="Data wykonanie", default=datetime.date.today)
    description = models.TextField(blank=True, verbose_name="Opis")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    crop_type = models.ForeignKey(
        CropType,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Roślina uprawna",
        help_text="Wymagane tyklo dla zbiegu typu siew",
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.treatment_type} - {self.field.name} ({self.date})"

    def clean(self):
        if self.treatment_type == self.TreatmentType.SOWING and not self.crop_type:
            raise ValidationError(
                {
                    "crop_type": "Musisz wybrać rośliną uprawną, jeśli chcesz dodać zabieg siewu"
                }
            )

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        self.full_clean()

        super().save(*args, **kwargs)

        if (
            is_new
            and self.treatment_type == self.TreatmentType.SOWING
            and self.crop_type
        ):
            Cultivation.objects.update_or_create(
                field=self.field,
                crop_type=self.crop_type,
                year=self.date.year,
                defaults={"sowing_date": self.date, "owner": self.field.owner},
            )
