from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from specs.models import *
from brandprofile.models import Brand
from .models import SearchProfile, SearchResult, ResultSpecs, AllowedSpecs
from .forms import CreateProfileForm, ProfileSearchForm, EmptyChoiceField
import requests
import json
import string
from django.http import JsonResponse


def create_profile(request):
    if request.method == 'POST':
        form = CreateProfileForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['new_brand']:
                brand = create_brand(cd['new_brand'])
            else:
                brand = Brand.objects.get(pk=cd['brand'])
            try:
                SearchProfile.objects.create(category=cd['category'], brand=brand)
            except IntegrityError as e:
                messages.info(request, f'Error: {e.__cause__}')
            return redirect('searchprofile:profile_list')
        else:
            messages.info(request, "Something went wrong, please notify the administrator")
        return render(request, 'searchprofile/createprofile.html', {'form': form})
    else:
        form = CreateProfileForm()
        return render(request, 'searchprofile/createprofile.html', {'form': form})


def create_brand(brand_name):
    code = "Brand={}".format(brand_name).replace(' ', '%2520').replace('&', '%26')
    keyword = brand_name.replace(' ', '+').replace('&', '%26')
    new_brand = brand_name
    new_brand = Brand.objects.create(name=string.capwords(brand_name), code=code, keyword=keyword)
    return new_brand


def profile_list(request):
    return render(request, 'searchprofile/profilelist.html', {'profiles': SearchProfile.objects.all()})


def profile_detail(request, profile_id):
    profile = SearchProfile.objects.get(pk=profile_id)
    spec_names = profile.get_allowed_spec_names()
    request.session['profile_id'] = profile.id
    request.session['category_code'] = profile.category.code
    request.session['spec_list'] = spec_names
    if 'spec_values' not in request.session:
        request.session['spec_values'] = ''
    form = add_dynamic_fields(request, ProfileSearchForm(), spec_names)
    results = SearchResult.objects.filter(profile=profile).prefetch_related()
    return render(request, 'searchprofile/profiledetail.html', {'profile': profile, 'form': form, 'results': results})


def add_dynamic_fields(request, form, spec_names):
    spec_values = {}
    if request.session['spec_values'] != '':
        spec_values = json.loads(request.session['spec_values'])
    else:
        spec_values['keywords'] = ''
    for spec in spec_names:
        spec_type = ContentType.objects.get(model=spec)
        spec_class = spec_type.model_class()
        if spec not in spec_values.keys():
            initial_value = ''
        else:
            initial_value = spec_values[spec]
        form.fields[spec] = EmptyChoiceField(choices=spec_class.objects.values_list('code', 'name'), required=False, initial=initial_value)
    if 'keywords' in form.fields.keys():
        form.fields['keywords'].initial = spec_values['keywords']
    return form


def create_search(request):
    profile = SearchProfile.objects.get(pk=request.session['profile_id'])
    if request.method == 'POST':
        url_string = build_url_string(request, profile)
        if url_string:
            data = get_search_data(url_string)
            search_result = SearchResult.objects.create(profile=profile, forsale=data['forsale'], avg_forsale_price=data['avg_forsale_price'],
                                                        sold=data['sold'], avg_sold_price=data['avg_sold_price'], ratio=data['ratio'],
                                                        search_url=url_string, keywords=request.POST['keywords'])
            spec_values = {}
            spec_values['keywords'] = request.POST['keywords']
            for spec in request.session['spec_list']:
                spec_type = ContentType.objects.get(model=spec)
                spec_class = spec_type.model_class()
                if request.POST[spec]:
                    value = spec_class.objects.values_list('name', flat=True).get(code=request.POST[spec])
                    ResultSpecs.objects.create(result=search_result, spec_name=spec, spec_value=value)
                    spec_values[spec] = request.POST[spec]
                else:
                    spec_values[spec] = ''
            spec_values = json.dumps(spec_values)
            request.session['spec_values'] = spec_values
            return redirect('searchprofile:profile_detail', profile_id=profile.id)
        else:
            messages.info(request, 'Select at least one specific to search for')
            form = ProfileSearchForm(spec_list=request.session['spec_list'])
            return render('searchprofile/profiledetail.html', {'profile': profile, 'form': form})
    return render(request, 'searchprofile/profiledetail.html', {'profile': profile, 'form': form})


def build_url_string(request, profile):
    url_string = f'https://www.ebay.com/sch/{profile.category.code}/i.html?{profile.brand.code}&LH_BIN=1'
    for spec in request.session['spec_list']:
        url_string += request.POST[spec]
    kw_string = f'&_nkw={profile.brand.keyword}+'
    if request.POST['keywords']:
        kw_string += request.POST['keywords'].strip().replace(', ', '+').replace(' ', '+').replace('&', '%26').replace('%', '%25')
    url_string += kw_string
    return url_string


def get_search_data(url_string):
    url = url = "https://ogboomer.pythonanywhere.com/fishapi/fishsearch/"
    search_response = requests.post(url, json=url_string)
    data = json.loads(search_response.content.decode('utf-8'))
    return data


def update_search(request, search_id):
    search_result = SearchResult.objects.get(pk=search_id)
    data = get_search_data(search_result.search_url)
    search_result.forsale = data['forsale']
    search_result.avg_forsale_price = data['avg_forsale_price']
    search_result.sold = data['sold']
    search_result.avg_sold_price = data['avg_sold_price']
    search_result.ratio = data['ratio']
    search_result.save()
    return redirect('searchprofile:profile_detail', request.session['profile_id'])


def delete_search(request, search_id):
    SearchResult.objects.filter(pk=search_id).delete()
    return redirect('searchprofile:profile_detail', request.session['profile_id'])


def jplay(request):
    return render(request, 'searchprofile/jayplay.html')
