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


class Size(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name
