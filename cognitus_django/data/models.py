from django.db import models


class Data(models.Model):
    text = models.CharField(
        max_length=64
    )
    label = models.CharField(
        max_length=16
    )

    def __str__(self):
        return f"{self.text} {self.label} "
