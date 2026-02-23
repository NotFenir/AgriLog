from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class CropType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Field(models.Model):
    name = models.CharField(max_length=100)
    area_size = models.DecimalField(max_digits=5, decimal_places=2)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="fields",
        blank=True,
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Cultivation(models.Model):
    class Status(models.TextChoices):
        PROGRESS = "PG", "W trakcie"
        COMPLETED = "CP", "Zakończono (zebrano)"
        CANCELLED = "CL", "Anulowano (nie przetrwaly)"

    field = models.ForeignKey(Field, on_delete=models.SET_NULL, null=True)
    crop_type = models.ForeignKey(CropType, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.PROGRESS
    )
    year = models.PositiveIntegerField()
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def is_active_now(self):
        return self.year == timezone.now().year
