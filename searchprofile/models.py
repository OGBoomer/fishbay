from django.db import models
from category.models import Category
from specs.models import SpecsList
from brandprofile.models import Brand

# Main object acted on for application


class SearchProfile(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('brand', 'category',)
        ordering = ['brand__name']

    def get_allowed_spec_names(self):
        spec_names = AllowedSpecs.objects.filter(category=self.category).prefetch_related('spec_names').values_list('spec__name', flat=True)
        spec_names = [spec_name.lower().replace(' ', '') for spec_name in spec_names]
        return spec_names

    def __str__(self):
        return f'{self.brand} -- {self.category}'


class SearchResult(models.Model):
    profile = models.ForeignKey(SearchProfile, on_delete=models.CASCADE, related_name='results')
    forsale = models.PositiveIntegerField(null=False)
    avg_forsale_price = models.FloatField(null=False)
    sold = models.PositiveIntegerField(null=False)
    avg_sold_price = models.FloatField(null=False)
    ratio = models.FloatField(null=False)
    search_url = models.URLField(max_length=300, null=False)
    keywords = models.TextField(null=True)
    last_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.profile} -- {self.last_updated}'


class ResultSpecs(models.Model):
    result = models.ForeignKey(SearchResult, on_delete=models.CASCADE, related_name='spec_line')
    spec_name = models.CharField(max_length=100, null=False)
    spec_value = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f'{self.spec_name} -- {self.spec_value}'


class AllowedSpecs(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    spec = models.ForeignKey(SpecsList, related_name='spec_id', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('category', 'spec',)

    def __str__(self):
        return f'{self.category} -- {self.spec}'
