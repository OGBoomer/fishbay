from django.db import models
from category.models import Category


class SizeList(models.Model):
    name = models.CharField(max_length=100, blank=True, unique=True, null=False)

    def __str__(self):
        return self.name


class AllowedSize(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeList, related_name='size_name', on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('category', 'size',)

    def __str__(self):
        return f'{self.category} -- {self.size}'


class MensSizeType(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class WomensSizeType(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class MensSize(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class MensBigTallSize(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class MensJeanSize(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class MensJeanBigTallSize(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name
