from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def total_area(self):
        return (
            self.user.fields.aggregate(models.Sum("area_size"))["area_size__sum"] or 0
        )
