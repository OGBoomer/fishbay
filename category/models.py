from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=100, blank=False)
    code = models.CharField(max_length=30, unique=True, blank=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return (self.name)
