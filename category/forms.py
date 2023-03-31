from django import forms


class CategoryAddNodeForm(forms.Form):
    name = forms.CharField(label="Category Name", max_length=200)
    code = forms.CharField(label="Ebay Category Id", max_length=50)
    parent_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
