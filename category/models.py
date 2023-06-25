from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class ItemType(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True, null=False)
    identifier = models.CharField(max_length=10, blank=False, unique=True, null=False)

    def __str__(self):
        return self.name


class Category(MPTTModel):
    name = models.CharField(max_length=100, blank=False)
    code = models.CharField(max_length=30, unique=True, blank=False)
    qualifier = models.CharField(max_length=100, null=True, blank=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.qualifier + ' ' + self.name
