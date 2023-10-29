from django.db import models

# A table for AllowedSpecs Table to match all Specs allowed in a Category
# Manual Admin entry must be made for each new spec class added.


class SpecsList(models.Model):
    name = models.CharField(max_length=100, blank=True, unique=True, null=False)

    def __str__(self):
        return self.name

# Below is a class for each type of specification(spec).
# An entry must be made in the SpecList Table for each new spec class added.
# the name in that table must match the Class name (spaces are allowed).
# code is the Ebay specific code added to url for the search (ex. &condition=1000)


class Condition(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=50, blank=True, null=False)

    def __str__(self):
        return self.name


class SleeveLength(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class Pattern(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class Fit(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class Neckline(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class WomensNeckline(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class Vintage(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class MensGenericFabric(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class MensPantRise(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class MensCollar(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class WomensSizeType(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class GenericSizeType(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class GenericSize(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)
    size_type = models.ForeignKey(GenericSizeType, null=False, on_delete=models.CASCADE, related_name='sizetype')

    def __str__(self):
        return self.name


class WomensTopSize(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=False, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)
    size_type = models.ForeignKey(WomensSizeType, null=False, on_delete=models.CASCADE, related_name='Womenssizetype')

    class Meta:
        unique_together = ('name', 'size_type')

    def __str__(self):
        return self.name


class WomensTopType(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class MensShirtNecksize(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class GenericFeature(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class MensPantSize(models.Model):
    name = models.CharField(max_length=50, blank=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)
    size_type = models.ForeignKey(GenericSizeType, null=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'size_type')

    def __str__(self):
        return self.name


class MensPantWaistSize(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class MensPantInseamSize(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class MensShortInseamSize(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class MensPantClosure(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class MensShortStyle(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class MensJacketStyle(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class JacketOuterShell(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class JacketLining(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class JacketInsulation(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class MensJacketType(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class MensJacketClosure(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
