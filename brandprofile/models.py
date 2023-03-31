from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100, blank=True, unique=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    keyword = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
