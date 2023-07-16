from django.db import models
from category.models import Category
from specs.models import *
from django.conf import settings
from size.models import *

# Main object acted on for application


class Brand(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='brand_user')
    name = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    keyword = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['name']

    def __str__(self):
        return self.name


class SearchProfile(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('brand', 'category', 'user')
        ordering = ['brand__name']

    def __str__(self):
        return f'{self.brand} - {self.category}'


class SearchResult(models.Model):
    profile = models.ForeignKey(SearchProfile, on_delete=models.CASCADE, related_name='results')
    forsale = models.PositiveIntegerField(null=False)
    avg_forsale_price = models.FloatField(null=False)
    sold = models.PositiveIntegerField(null=False)
    avg_sold_price = models.FloatField(null=False)
    ratio = models.FloatField(null=False)
    search_url = models.URLField(max_length=350, null=False)
    keywords = models.CharField(max_length=250, blank=True, null=True)
    heading = models.CharField(max_length=200, null=False)
    last_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.profile} -- {self.last_updated}'


class ProfileModel(models.Model):
    profile = models.ForeignKey(SearchProfile, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100, null=False)
    code = models.CharField(max_length=100, null=False)

    class Meta:
        ordering = ['name']
        unique_together = ('profile', 'name',)

    def __str__(self):
        return self.name


class MensClothingItem(models.Model):
    vintage = models.CharField(max_length=30, blank=True, null=True)
    condition = models.CharField(max_length=30, blank=True, null=True)
    size_type = models.CharField(max_length=30, blank=True, null=True)
    size = models.CharField(max_length=30, blank=True, null=True)
    material = models.CharField(max_length=30, blank=True, null=True)
    pattern = models.CharField(max_length=30, blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True)
    fit = models.CharField(max_length=30, blank=True, null=True)
    fabric = models.CharField(max_length=30, blank=True, null=True)
    item_model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        abstract = True


class GenericMensTop(MensClothingItem):
    sleeve_length = models.CharField(max_length=30, blank=True, null=True)
    collar = models.CharField(max_length=30, blank=True, null=True)
    result = models.ForeignKey(SearchResult, on_delete=models.CASCADE, null=False)


class GenericMensPolo(GenericMensTop):
    neckline = models.CharField(max_length=50, blank=True, null=True)


class GenericMensPant(MensClothingItem):
    waist_size = models.CharField(max_length=20, blank=True, null=True)
    inseam = models.CharField(max_length=20, blank=True, null=True)
    rise = models.CharField(max_length=20, blank=True, null=True)
    closure = models.CharField(max_length=20, blank=True, null=True)
    result = models.ForeignKey(SearchResult, on_delete=models.CASCADE, null=False)


class GenericMensShort(GenericMensPant):
    style = models.CharField(max_length=20, blank=True, null=True)
