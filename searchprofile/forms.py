from django import forms
from django.forms import ModelForm
from django.contrib.contenttypes.models import ContentType
from .models import *
from category.models import Category
from specs.models import *
from mptt.forms import TreeNodeChoiceField
from django.core.exceptions import ValidationError
from django.contrib import messages

# A custom form field class to allow a none selection from a forms.ChoiceField
# credit davidbgk at https://gist.github.com/davidbgk/651080


class EmptyChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), empty_label=u"-----", required=True, widget=None, label=None,
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
# allows the selection of an exising Brand or the creation of a new one


class CreateProfileForm(forms.Form):
    new_brand = forms.CharField(max_length=50, label='or New Brand', required=False)
    category = TreeNodeChoiceField(queryset=Category.objects.filter(children__isnull=True), required=False, level_indicator='')
    # brand = EmptyChoiceField(choices=Brand.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CreateProfileForm, self).__init__(*args, **kwargs)
        qs = Brand.objects.filter(user=self.user).values_list('id', 'name')
        self.fields['brand'] = EmptyChoiceField(choices=qs, required=False)

    class Meta:
        fields = {'brand', 'new_brand', 'category'}

    def clean(self):
        # Custom Validation
        cd = self.cleaned_data

        # need to find out why 'category' is missing from cleaned data if null (workaround)
        if 'category' not in cd:
            cd['category'] = ''
            raise ValidationError('Selecting a Category is required.')

        # depreciated, currently only leaf nodes are available for selection
        # if not cd['category'].is_leaf_node():
        #    raise ValidationError('Category too broad, drill down')

        # must include brand from drop down or enter a new one
        if not cd['new_brand'] and not cd['brand']:
            raise ValidationError('Must either select Brand from dropdown or enter a new one.')
        # but not both
        if cd['new_brand'] and cd['brand']:
            raise ValidationError('Select Brand from dropdown OR type a new one, not both.')
        try:
            brand = Brand.objects.get(name__iexact=cd['new_brand'], user=self.user)
            # if new brand exists make adjustments
            cd['brand'] = brand.id
            cd['new_brand'] = ''
        except Brand.DoesNotExist:
            # if it doesn't exist continue as normal
            pass
        return cd


class CreateBrandForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)

# Form on the details page which allowes a new search to be added


class GenericMensClothingForm(forms.Form):
    vintage = forms.BooleanField(required=False)
    condition = EmptyChoiceField(choices=Condition.objects.values_list('code', 'name'), required=False)
    size_type = EmptyChoiceField(choices=GenericSizeType.objects.values_list('code', 'name'), required=False)
    size = EmptyChoiceField(required=False)
    material = EmptyChoiceField(choices=Material.objects.values_list('code', 'name'), required=False)
    pattern = EmptyChoiceField(widget=forms.Select(attrs={'onFocus': 'changeSize();', 'onBlur': 'doBlue();'}), choices=Pattern.objects.values_list('code', 'name'), required=False)
    color = EmptyChoiceField(choices=Color.objects.values_list('code', 'name'), required=False)
    fit = EmptyChoiceField(choices=Fit.objects.values_list('code', 'name'), required=False)
    fabric = EmptyChoiceField(choices=MensGenericFabric.objects.values_list('code', 'name'), required=False)
    item_model = EmptyChoiceField(label='Model', required=False)

    def __init__(self, *args, **kwargs):
        # kwargs should contain a profile variable AND either an item_type variable
        # OR form data in the data variable that will contain the item_type.
        self.profile = kwargs.pop('profile', None)
        self.data = kwargs['data']
        self.item_type = kwargs.pop('item_type', None)
        if not self.item_type:
            self.item_type = self.data['item_type']
        super().__init__(*args, **kwargs)
        self.fields['size_type'].widget.attrs.update({
            'hx-post': "/search/updatesize/",
            'hx-trigger': 'change',
            'hx-target': '#size',
            'hx-swap': 'innerHTML'
        })
        if 'size' in self.data:
            # size was passed in the form check if it has a value
            if self.data['size']:
                print(f'size is {self.data["size"]}')
                sizeqs = get_size_qs_by_type(self.data['size_type'], self.data['item_type'])
                self.fields['size'] = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size': '1', 'onFocus': 'growSize(event);', 'onBlur': 'shrinkSize(event);'}), choices=sizeqs, initial=self.data['size'], required=False)
        try:
            itemqs = ProfileModel.objects.filter(profile=self.profile).values_list('code', 'name')
        except ProfileModel.DoesNotExist:
            itemqs = ''
        self.fields['item_model'] = EmptyChoiceField(choices=itemqs, label='Model', required=False)
        self.fields['profile_id'] = forms.IntegerField(initial=self.profile.id, label='', widget=forms.HiddenInput())
        self.fields['item_type'] = forms.CharField(initial=self.item_type, label='', widget=forms.HiddenInput())


class WomensClothingForm(GenericMensClothingForm):
    size_type = EmptyChoiceField(choices=WomensSizeType.objects.values_list('code', 'name'), required=False)


class GenericMensTopForm(GenericMensClothingForm):
    sleeve_length = EmptyChoiceField(choices=SleeveLength.objects.values_list('code', 'name'), required=False)
    collar = EmptyChoiceField(choices=MensCollar.objects.values_list('code', 'name'), required=False)
    keywords = forms.CharField(max_length=250, required=False)
    field_order = ['vintage', 'condition', 'size_type', 'size', 'sleeve_length', 'fit', 'collar', 'pattern', 'material', 'fabric', 'color', 'item_model']


class WomensTopForm(WomensClothingForm):
    sleeve_length = EmptyChoiceField(choices=SleeveLength.objects.values_list('code', 'name'), required=False)
    top_type = EmptyChoiceField(choices=WomensTopType.objects.values_list('code', 'name'), required=False, label='Type')
    neckline = EmptyChoiceField(choices=WomensNeckline.objects.values_list('code', 'name'), required=False)
    keywords = forms.CharField(max_length=250, required=False)
    field_order = ['vintage', 'condition', 'size_type', 'size', 'top_type', 'sleeve_length', 'neckline', 'fit', 'pattern', 'material', 'fabric', 'color', 'item_model']


class WomensDressForm(WomensClothingForm):
    fit = None
    sleeve_length = EmptyChoiceField(choices=SleeveLength.objects.values_list('code', 'name'), required=False)
    dress_style = EmptyChoiceField(choices=DressStyle.objects.values_list('code', 'name'), required=False, label='Style')
    dress_length = EmptyChoiceField(choices=DressLength.objects.values_list('code', 'name'), required=False, label='Length')
    neckline = EmptyChoiceField(choices=WomensNeckline.objects.values_list('code', 'name'), required=False)
    keywords = forms.CharField(max_length=250, required=False)
    field_order = ['vintage', 'condition', 'size_type', 'size', 'dress_style', 'dress_length', 'sleeve_length', 'neckline', 'pattern', 'material', 'fabric', 'color', 'item_model']


class GenericMensPoloForm(GenericMensTopForm):
    neckline = EmptyChoiceField(choices=Neckline.objects.values_list('code', 'name'), required=False)

    field_order = ['vintage', 'condition', 'size_type', 'size', 'sleeve_length', 'fit', 'collar', 'neckline', 'pattern', 'material', 'fabric', 'color', 'item_model']


class MensDressShirtForm(GenericMensTopForm):
    neck_size = EmptyChoiceField(choices=MensShirtNecksize.objects.values_list('code', 'name'), required=False)

    field_order = ['vintage', 'condition', 'size_type', 'size', 'neck_size', 'sleeve_length', 'fit', 'collar', 'pattern', 'material', 'fabric', 'color', 'item_model']


class MensHoodiesSweatshirtsForm(GenericMensTopForm):
    feature = EmptyChoiceField(choices=GenericFeature.objects.values_list('code', 'name'), required=False)

    field_order = ['vintage', 'condition', 'size_type', 'size', 'sleeve_length', 'fit', 'collar', 'neckline', 'feature', 'pattern', 'material', 'fabric', 'color', 'item_model']


class GenericMensPantForm(GenericMensClothingForm):
    waist_size = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size': '1', 'onFocus': 'growSize(event);', 'onBlur': 'shrinkSize(event);'}), choices=MensPantWaistSize.objects.values_list('code', 'name'), required=False)
    inseam = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size': '1', 'onFocus': 'growSize(event);', 'onBlur': 'shrinkSize(event);'}), choices=MensPantInseamSize.objects.values_list('code', 'name'), required=False)
    rise = EmptyChoiceField(choices=MensPantRise.objects.values_list('code', 'name'), required=False)
    closure = EmptyChoiceField(choices=MensPantClosure.objects.values_list('code', 'name'), required=False)
    keywords = forms.CharField(max_length=250, required=False)

    field_order = ['vintage', 'condition', 'size_type', 'size', 'waist_size', 'inseam', 'closure', 'rise', 'fit', 'neckline', 'pattern', 'material', 'fabric', 'color', 'item_model']


class JeansForm(GenericMensPantForm):
    jeans_style = EmptyChoiceField(choices=JeansStyle.objects.values_list('code', 'name'), required=False, label='Style')

    field_order = ['vintage', 'condition', 'size_type', 'size', 'waist_size', 'inseam', 'jeans_style', 'closure', 'rise', 'fit', 'neckline', 'pattern', 'material', 'fabric', 'color', 'item_model']


class GenericMensShortForm(GenericMensPantForm):
    style = EmptyChoiceField(choices=MensShortStyle.objects.values_list('code', 'name'), required=False)
    inseam = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size': '1', 'onFocus': 'growSize(event);', 'onBlur': 'shrinkSize(event);'}), choices=MensShortInseamSize.objects.values_list('code', 'name'), required=False)

    field_order = ['vintage', 'condition', 'size_type', 'size', 'waist_size', 'inseam', 'style', 'closure', 'rise', 'fit', 'neckline', 'pattern', 'material', 'fabric', 'color', 'item_model']


class MensJacketForm(GenericMensTopForm):
    jacket_type = EmptyChoiceField(choices=MensJacketType.objects.values_list('code', 'name'), required=False, label='Type')
    shell = EmptyChoiceField(choices=JacketOuterShell.objects.values_list('code', 'name'), required=False)
    lining = EmptyChoiceField(choices=JacketLining.objects.values_list('code', 'name'), required=False)
    insulation = EmptyChoiceField(choices=JacketInsulation.objects.values_list('code', 'name'), required=False)
    style = EmptyChoiceField(choices=MensJacketStyle.objects.values_list('code', 'name'), required=False)
    closure = EmptyChoiceField(choices=MensJacketClosure.objects.values_list('code', 'name'), required=False)

    field_order = ['vintage', 'condition', 'size_type', 'size', 'jacket_type', 'style', 'closure', 'pattern', 'shell', 'lining', 'insulation', 'material', 'fabric', 'color', 'item_model']


class SizeUpdateForm(forms.Form):
    size = EmptyChoiceField(required=False)

    def update_size(self, size_type, item_type):
        qs = get_size_qs_by_type(size_type, item_type)
        self.fields['size'] = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size': '1', 'onFocus': 'growSize(event);', 'onBlur': 'shrinkSize(event);'}), choices=qs, required=False)


def get_size_qs_by_type(size_type, item_type):
    match item_type:
        case 'GMT' | 'GMO' | 'CJV' | 'MAT' | 'MHS' | 'MDS' | 'MTS' | 'MST':
            size_type = GenericSizeType.objects.get(code=size_type)
            qs = GenericSize.objects.filter(size_type=size_type).values_list('code', 'name')
        case 'GMP' | 'GMS' | 'MAP' | 'MPT':
            size_type = GenericSizeType.objects.get(code=size_type)
            qs = MensPantSize.objects.filter(size_type=size_type).values_list('code', 'name')
        case 'WTP' | 'DRS' | 'WJN':
            size_type = WomensSizeType.objects.get(code=size_type)
            qs = WomensTopSize.objects.filter(size_type=size_type).values_list('code', 'name')
        case _:
            print('no match')
            qs = ''
    return qs


class ProfileSearchForm(forms.Form):
    # Pass through variables, would possible better to store in session
    brand = forms.CharField(max_length=100, widget=forms.HiddenInput)
    category = forms.CharField(max_length=200, widget=forms.HiddenInput)
    profile_id = forms.IntegerField(widget=forms.HiddenInput)
    search_id = forms.IntegerField(widget=forms.HiddenInput)
    keywords = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, "cols": 20}), help_text='Comma seperated list', required=False)
