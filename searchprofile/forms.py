from django import forms
from django.contrib.contenttypes.models import ContentType
from .models import SearchProfile
from category.models import Category
from specs.models import *
from brandprofile.models import Brand
from mptt.forms import TreeNodeChoiceField
from django.core.exceptions import ValidationError

# A custom form field class to allow a none selection from a forms.ChoiceField


class EmptyChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), empty_label=u"---------", required=True, widget=None, label=None,
                 initial=None, help_text=None, *args, **kwargs):

        # prepend an empty label unless the field is required AND
        # an initial value is supplied

        if required and (initial is not None):
            pass  # don't prepend the empty label
        else:
            choices = tuple([(u'', empty_label)] + list(choices))

        super(EmptyChoiceField, self).__init__(choices=choices, required=required, widget=widget, label=label,
                                               initial=initial, help_text=help_text, *args, **kwargs)

# Create a new object that searches can anchored to
# allows the selection of an exising Brand or the createion of a new one


class CreateProfileForm(forms.Form):
    new_brand = forms.CharField(max_length=50, label='or New Brand', required=False)
    category = TreeNodeChoiceField(queryset=Category.objects.all())
    brand = EmptyChoiceField(choices=Brand.objects.values_list('id', 'name'), required=False)

    class Meta:
        fields = {'brand', 'new_brand', 'category'}

    def clean(self):
        # Custom Validation
        cd = self.cleaned_data
        # One or the other needs to have a value
        if not cd['new_brand'] and not cd['brand']:
            raise ValidationError('Must either select Brand from dropdown or enter a new one.')
        # They can't both have a value
        if cd['new_brand'] and cd['brand']:
            raise ValidationError('Select Brand from dropdown OR type a new one, not both.')
        # If new Brand make sure it doesn't already exist
        if Brand.objects.filter(name__iexact=cd['new_brand']).exists():
            raise ValidationError('Brand already exists select it from dropdown')
        return cd

# Form on the details page which allowes a new search to be added


class ProfileSearchForm(forms.Form):
    # Pass through variables, would possible better to store in session
    brand = forms.CharField(max_length=100, widget=forms.HiddenInput)
    category = forms.CharField(max_length=200, widget=forms.HiddenInput)
    profile_id = forms.IntegerField(widget=forms.HiddenInput)
    search_id = forms.IntegerField(widget=forms.HiddenInput)
    keywords = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, "cols": 20}), help_text='Comma seperated list', required=False)
