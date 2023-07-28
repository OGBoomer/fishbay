from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.mail import send_mail
from O365 import Account
from specs.models import *
from .models import *
from .forms import *
import requests
import json
import string
import re
import copy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from render_block import render_block_to_string


@login_required()
def profile_list(request):
    if request.method == 'POST':
        form = CreateProfileForm(request.POST, user=request.user)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['new_brand']:
                brand = create_brand(cd['new_brand'], request.user)
            else:
                brand = Brand.objects.get(pk=cd['brand'])
            try:
                SearchProfile.objects.create(category=cd['category'], brand=brand, user=request.user)
                request.session['notice'] = 'Profile Added1'
                triggers = '{"check_notice": "", "profile_added": ""}'
            except IntegrityError as e:
                request.session['notice'] = 'Profile already exists.'
                triggers = 'check_notice'
            context = {'form': CreateProfileForm(user=request.user)}
        else:
            context = {'form': CreateProfileForm(request.POST, user=request.user)}
        html = render_block_to_string('searchprofile/profilelist.html', 'profile-form', context)
        response = HttpResponse(html)
        response['HX-Trigger'] = triggers
        return response
    else:
        print('oops')
        context = {
            'form': CreateProfileForm(user=request.user),
            'profiles': SearchProfile.objects.filter(brand__name__istartswith='', user=request.user,)
        }
    return render(request, 'searchprofile/profilelist.html', context)


@login_required()
def brand_list(request):
    if request.method == 'POST':
        form = CreateBrandForm(request.POST)
        if form.is_valid():
            triggers = '{"check_notice": "", "brand_added": ""}'
            cd = form.cleaned_data
            create_brand(cd['name'], request.user)
            context = {'form': CreateBrandForm()}
        else:
            context = {'form': CreateBrandForm()}
        html = render_block_to_string('searchprofile/brandlist.html', 'brand-form', context)
        response = HttpResponse(html)
        response['HX-Trigger'] = triggers
        return response
    else:
        context = {
            'form': CreateBrandForm(),
            'brands': Brand.objects.filter(user=request.user)
        }
    return render(request, 'searchprofile/brandlist.html', context)


def update_profile_list(request):
    if request.method == 'POST':
        filter_text = request.POST['filter_text']
    else:
        filter_text = ''
    context = {'profiles': SearchProfile.objects.filter(brand__name__istartswith=filter_text, user=request.user,)}
    html = render_block_to_string('searchprofile/profilelist.html', 'profile-list', context)
    response = HttpResponse(html)
    if request.session['notice'] == 'Profile Added1':
        request.session['notice'] = 'Profile Added'
        response['HX-Trigger'] = 'check_notice'
    else:
        request.session['notice'] = ''
    return response


def update_brand_list(request):
    request.session['notice'] = 'Brand created.'
    context = {'brands': Brand.objects.filter(user=request.user)}
    html = render_block_to_string('searchprofile/brandlist.html', 'brand-list', context)
    response = HttpResponse(html)
    response['HX-Trigger'] = 'check_notice'
    return response


@ login_required()
def delete_profile(request, profile_id):
    SearchProfile.objects.filter(pk=profile_id).delete()
    request.session['notice'] = 'Profile deleted.'
    html = '<div></div>'
    response = HttpResponse(html)
    response['HX-Trigger'] = 'check_notice'
    return response


@ login_required()
def delete_brand(request, brand_id):
    Brand.objects.filter(pk=brand_id).delete()
    request.session['notice'] = 'Brand deleted.'
    html = '<div></div>'
    response = HttpResponse(html)
    response['HX-Trigger'] = 'check_notice'
    return response


@login_required()
def profile_detail(request, profile_id):
    profile = SearchProfile.objects.get(pk=profile_id)
    form = get_form_by_type(profile=profile)
    results = SearchResult.objects.filter(profile=profile)
    context = {
        'profile': profile,
        'form': form,
        'results': results
    }
    html = render_block_to_string('searchprofile/profiledetail.html', 'content', context)
    return HttpResponse(html)


def get_form_by_type(profile_id='', profile='', form_data=''):
    print(form_data)
    if profile == '':
        if profile_id == '':
            profile_id = form_data['profile_id']
        profile = SearchProfile.objects.get(pk=profile_id)
    if form_data == '':
        item_type = profile.category.item_type.identifier
        field_data = {'profile_id': profile.id, 'item_type': item_type}
    else:
        item_type = form_data['item_type']
        field_data = form_data
    match item_type:
        case 'GMT' | 'MAT' | 'MTS' | 'MST':
            form = GenericMensTopForm(data=field_data, profile=profile)
        case 'GMP' | 'MAP' | 'MPT':
            form = GenericMensPantForm(data=field_data, profile=profile)
        case 'GMO':
            form = GenericMensPoloForm(data=field_data, profile=profile)
        case 'GMS':
            form = GenericMensShortForm(data=field_data, profile=profile)
        case 'CJV':
            form = MensJacketForm(data=field_data, profile=profile)
        case 'MHS':
            form = MensHoodiesSweatshirtsForm(data=field_data, profile=profile)
        case 'MDS':
            form = MensDressShirtForm(data=field_data, profile=profile)
        case _:
            pass
    return form


@login_required()
def brand_detail(request, brand_id):
    brand = Brand.objects.get(pk=brand_id)
    profiles = SearchProfile.objects.filter(user=request.user, brand=brand_id).prefetch_related('results')
    context = {
        'brand': brand,
        'profiles': profiles
    }
    return render(request, 'searchprofile/branddetail.html', context)


def update_size(request):
    form = SizeUpdateForm()
    form.update_size(request.POST['size_type'], request.POST['item_type'])
    context = {
        'form': form
    }
    html = render_block_to_string('searchprofile/size.html', 'size_field', context)
    return HttpResponse(html)


@login_required()
def create_search(request):
    profile = SearchProfile.objects.get(pk=request.POST['profile_id'])
    if request.method == 'POST':
        form = get_form_by_type(form_data=request.POST, profile=profile)
        if form.is_valid():
            # form = GenericMensTopForm(request.POST, profile=profile)
            url_string = build_url_string(copy.deepcopy(form.cleaned_data), profile)
            if url_string:
                data = get_search_data(url_string)
                heading = build_search_heading(copy.deepcopy(form.cleaned_data))
                search_result = SearchResult.objects.create(profile=profile, forsale=data['forsale'], avg_forsale_price=data['avg_forsale_price'],
                                                            sold=data['sold'], avg_sold_price=data['avg_sold_price'], ratio=data['ratio'],
                                                            search_url=url_string, keywords=request.POST['keywords'], heading=heading)
                create_item(copy.deepcopy(form.cleaned_data), search_result)
                triggers = '{"check_notice": "", "result_added": ""}'
            else:
                messages.info(request, 'Problem contact administrator')
        else:
            messages.info(request, 'Problem contact administrator')
    else:
        form = get_form_by_type(profile=profile)
        # form = GenericMensTopForm(profile=profile)
        triggers = ''
    context = {
        'profile': profile,
        'form': form
    }
    request.session['notice'] = 'New search added.'
    html = render_block_to_string('searchprofile/profiledetail.html', 'search-form', context)
    response = HttpResponse(html)
    # format for multiple triggers MUST be single quote JSON string with double quotes for JSON
    response['HX-Trigger'] = triggers
    return response


def create_brand(brand_name, user):
    code = "Brand={}".format(brand_name).replace(' ', '%2520').replace('&', '%26').replace('\'', '%2527')
    keyword = brand_name.replace(' ', '+').replace('&', '%2526')
    new_brand = brand_name
    new_brand = Brand.objects.create(name=brand_name, code=code, keyword=keyword, user=user)
    return new_brand


def create_item(form_data, result):
    data = {}
    form_data.pop('keywords', None)
    form_data.pop('profile_id', None)
    vint = form_data.pop('vintage', None)
    if vint:
        data['vintage'] = 'Yes'
    item = get_object_by_type(form_data['item_type'], result)
    for (key, value) in form_data.items():
        if value != '':
            if key == 'condition':
                value = list(Condition.objects.filter(code=value).values_list('name', flat=True))[0]
            else:
                if isinstance(value, list):
                    if len(value) > 1:
                        new_value = strip_codes(value.pop(0))
                        for item_value in value:
                            new_value += '-' + strip_codes(item_value)
                        value = new_value
                    else:
                        if len(value) > 0:
                            value = strip_codes(value[0])
                        else:
                            value = ''
                else:
                    value = strip_codes(value)
            if value != '':
                data[key] = value
    for attr, val in data.items():
        setattr(item, attr, val)
    item.save()
    return item


def get_object_by_type(item_type, result):
    match item_type:
        case 'GMT':
            item_object = GenericMensTop.objects.create(result=result)
        case 'GMP' | 'MPT':
            item_object = GenericMensPant.objects.create(result=result)
        case 'GMO':
            item_object = GenericMensPolo.objects.create(result=result)
        case 'GMS':
            item_object = GenericMensShort.objects.create(result=result)
        case 'CJV':
            item_object = GenericMensJacket.objects.create(result=result)
        case 'MAT':
            item_object = MensActivewearTop.objects.create(result=result)
        case 'MAP':
            item_object = MensActivewearPant.objects.create(result=result)
        case 'MHS':
            item_object = MensHoodiesSweatshirts.objects.create(result=result)
        case 'MDS':
            item_object = MensDressShirt.objects.create(result=result)
        case 'MTS':
            item_object = MensDressShirt.objects.create(result=result)
        case 'MST':
            item_object = MensDressShirt.objects.create(result=result)
        case _:
            pass
    return item_object


def build_search_heading(form_data):
    result_heading = []
    keys_for_removal = ['keywords', 'profile_id', 'item_type']
    form_data = {key: value for key, value in form_data.items() if key not in keys_for_removal}
    for (key, value) in form_data.items():
        if value != '':
            if key == 'vintage':
                if value is True:
                    result_heading.append('VTG')
            elif key == 'condition':
                if value != '':
                    result_heading.append(list(Condition.objects.filter(code=value).values_list('name', flat=True))[0])
            else:
                new_value = value
                if isinstance(value, list):
                    new_value = ''
                    if len(value) > 1:
                        new_value = strip_codes(value.pop(0))
                        for item in value:
                            new_value += '-' + strip_codes(item)
                    else:
                        if len(value) > 0:
                            new_value = strip_codes(value[0])
                    if new_value != '':
                        result_heading.append(new_value)
                else:
                    result_heading.append(strip_codes(value))
    return '/'.join(result_heading)


def strip_codes(value):
    value = value.partition('=')[2].replace('%2520', ' ').replace('%2527', '\'').replace('%2526', '&').replace('%252D', '-')
    return value


def build_url_string(post_items, profile):
    print(f'post items is {post_items}')
    post_items.pop('profile_id', None)
    post_items.pop('item_type', None)
    url_string = f'https://www.ebay.com/sch/{profile.category.code}/i.html?{profile.brand.code}&_dcat={profile.category.code}&LH_BIN=1&_ipg=240&LH_PrefLoc=1'
    for key, value in post_items.items():
        if value != '':
            if key == 'vintage':
                if value is True:
                    url_string += '&Vintage=Yes'
                else:
                    value = ''
            elif key == 'keywords':
                url_string += '&_nkw=' + value
            elif isinstance(value, list):
                if len(value) > 1:
                    new_value = value.pop(0)
                    for item in value:
                        new_value += re.sub(r'^.*?=', '%7C', item)
                    url_string += new_value
                else:
                    if len(value) > 0:
                        url_string += value[0]
            else:
                if value != '':
                    url_string += value
    return url_string


def get_search_data(url_string):
    url = "https://ogboomer.pythonanywhere.com/fishapi/fishsearch/"
    search_response = requests.post(url, json=url_string)
    data = json.loads(search_response.content.decode('utf-8'))
    return data


@ login_required()
def update_search(request, search_id):
    search_result = SearchResult.objects.get(pk=search_id)
    data = get_search_data(search_result.search_url)
    search_result.forsale = data['forsale']
    search_result.avg_forsale_price = data['avg_forsale_price']
    search_result.sold = data['sold']
    search_result.avg_sold_price = data['avg_sold_price']
    search_result.ratio = data['ratio']
    search_result.save()
    context = {
        'result': search_result
    }
    request.session['notice'] = 'Search updated.'
    html = render_block_to_string('searchprofile/result.html', 'result-item', context)
    response = HttpResponse(html)
    response['HX-Trigger'] = 'check_notice'
    return response


@ login_required()
def delete_search(request, search_id):
    SearchResult.objects.filter(pk=search_id).delete()
    request.session['notice'] = 'Search deleted.'
    html = '<div></div>'
    response = HttpResponse(html)
    response['HX-Trigger'] = 'check_notice'
    return response


def update_result_list(request, profile_id):
    profile = SearchProfile.objects.get(pk=profile_id)
    context = {'results': SearchResult.objects.filter(profile=profile).prefetch_related()}
    html = render_block_to_string('searchprofile/profiledetail.html', 'result-list', context)
    return HttpResponse(html)


@ login_required()
def model_detail(request, profile_id):
    if request.method == 'POST':
        triggers = '{"check_notice": "", "model_added": ""}'
        model_name = request.POST['modelname']
        profile = SearchProfile.objects.get(pk=profile_id)
        code = '&Model=' + model_name.replace('\'', '%2527').replace(' ', '%2520')
        try:
            ProfileModel.objects.create(profile=profile, name=model_name, code=code)
        except IntegrityError as e:
            request.session['notice'] = 'Integrity Error. Try again or contact administrator'
            triggers = 'check_notice'
        context = {'profile': profile}
        html = render_block_to_string('searchprofile/models.html', 'model-form', context)
        response = HttpResponse(html)
        response['HX-Trigger'] = triggers
        return response
    else:
        profile = SearchProfile.objects.get(pk=profile_id)
        context = {
            'profile': profile,
            'profilemodels': ProfileModel.objects.filter(profile=profile)
        }
    return render(request, 'searchprofile/models.html', context)


def update_model_list(request, profile_id):
    profile = SearchProfile.objects.get(pk=profile_id)
    context = {
        'profile': profile,
        'profilemodels': ProfileModel.objects.filter(profile=profile)
    }
    request.session['notice'] = 'New model added.'
    html = render_block_to_string('searchprofile/models.html', 'model-list', context)
    response = HttpResponse(html)
    response['HX-Trigger'] = 'check_notice'
    return response


def delete_model(request, profile_id, model_id):
    profile = SearchProfile.objects.get(pk=profile_id)
    try:
        ProfileModel.objects.filter(pk=model_id).delete()
    except IntegrityError:
        pass
    context = {
        'profile': profile,
        'profilemodels': ProfileModel.objects.filter(profile=profile_id)
    }
    request.session['notice'] = 'Model deleted.'
    html = render_block_to_string('searchprofile/models.html', 'model-list', context)
    response = HttpResponse(html)
    response['HX-Trigger'] = 'check_notice'
    return response


def check_notice(request):
    context = {
        'notice': request.session['notice']
    }
    request.session['notice'] = ''
    html = render_block_to_string('searchprofile/profiledetail.html', 'notice', context)
    return HttpResponse(html)


def jplay(request):
    # data_listpattern = ['Animal Print','Argyle/Diamond','Camouflage','Colorblock','Fair Isle','Floral','Geometric','Herringbone','Paisley','Plaid','Polka Dot','Solid','Striped']
    # data_listsize = ['24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','XS','S','M','L','XL','2XL','3XL']
    # data_listbtsize = ['20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','48','50','52','54','56']
    # data_listinseam = ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37']
    # size_type = GenericSizeType.objects.get(name='Regular')
    # data_listfit = ['Athletic', 'Classic', 'Regular', 'Relaxed', 'Slim']
    # data_listvintage = ['Yes', 'No']
    # data_listmaterial = ['Acrylic', 'Alfa', 'Alginate', 'Alpaca', 'Angora', 'Aramid', 'Bamboo', 'Camel',
    # 'Cashmere', 'Cotton', 'Cotton Blend', 'Cupro', 'Elastodiene', 'Faux Fur', 'Flax',
    # 'Fur', 'Hemp', 'Leather', 'Linen', 'Lyocell', 'Modacrylic', 'Modal', 'Nylon',
    # 'Patent Leather', 'Polyacrylate Fiber', 'Polyamide', 'Polycarbamide', 'Polyester',
    # 'Polyester Blend', 'Polyethylene', 'Polylactide', 'Polyurethane', 'Ramie', 'Silk',
    # 'Spandex', 'Suede', 'Viscose', 'Wool']
    # data_listshell = ['Acelate', 'Alpaca', 'Angora', 'Animal Hair', 'Bamboo', 'Camel',
    #              'Cashmere', 'Cotton', 'Cotton Blend', 'Cupro', 'Elastodiene', 'Faux Fur', 'Flax Fur',
    #              'Fur', 'Hemp', 'Leather', 'Linen', 'Llama', 'Lyocell', 'Modacrylic', 'Modal', 'Mohair', 'Nylon',
    #              'Patent Leather', 'Polyamide', 'Polyester', 'Polyethylene', 'Polyimide', 'Polylactide', 'Polypropylene',
    #              'Polyurethane', 'PVC', 'Ramie', 'Silk', 'Spandex', 'Suede', 'Tweed', 'Twill', 'Velour', 'Velvet', 'Viscose',
    #              'Wool', 'Yak']
    # data_list = ['Acelate', 'Acrylic', 'Alpaca', 'Angora', 'Animal Hair', 'Bamboo', 'Camel',
    #             'Cashgora', 'Cashmere', 'Coir', 'Cotton', 'Cupro', 'Elastodiene', 'Faux Fur', 'Faux Leather', 'Flax',
    #             'Fur', 'Hemp', 'Leather', 'Linen', 'Llama', 'Lyocell', 'Modacrylic', 'Modal', 'Mohair', 'Nylon',
    #             'Patent Leather', 'Polyamide', 'Polyester', 'Polyethylene', 'Polyimide', 'Polylactide', 'Polypropylene',
    #             'Polyurethane', 'Ramie', 'Silk', 'Spandex', 'Suede', 'Tweed', 'Twill', 'Viscose', 'Wool', 'Yak']
    # data_listcolor = ['Beige', 'Black', 'Blue', 'Brown', 'Clear', 'Gold', 'Gray', 'Green', 'Ivory', 'Multicolor', 'Orange', 'Pink', 'Purple', 'Red', 'Silver', 'White', 'Yellow']
    # data_listcollar = ['Band', 'Button-Down', 'Cutaway', 'Point', 'Sailor', 'Spread', 'Stand-Up', 'Wing']
    # data_listfit = ['Athletic', 'Classic', 'Extra Slim', 'Regular', 'Relaxed', 'Slim']
    # data_listrise = ['Ultra Low', 'Low', 'Mid', 'High']
    # data_listfabric = ['Canvas', 'Chambray', 'Chiffon', 'Corduroy', 'Crochet', 'Damask', 'Denim', 'Down',
    #              'Flannel', 'Fleece', 'Jersey', 'Knit', 'Lace', 'Microfiber', 'Rayon', 'Satin', 'Tweed',
    #              'Twill', 'Velvet', 'Woven']
    # data_listneckline = ['Boat Neck', 'Collared', 'Cowl Neck', 'Crew Neck', 'Halter', 'Henley', 'High Neck',
    #              'Mock Neck', 'Round Neck', 'Scoop Neck', 'Square Neck', 'Sweetheart', 'Turtleneck',
    #              'V-Neck']
    # data_listclosure = ['Buckle', 'Button', 'Drawstring', 'Hook & Eye', 'Hook & Loop', 'Lace Up', 'Snap', 'Tie', 'Zip']
    # data_listshortstype = ['Bermuda', 'Biker', 'Cargo', 'Chino', 'Sweat']
    # data_listjackettype = ['Blazer', 'Cape', 'Coat', 'Coatigan', 'Jacket', 'Poncho', 'Vest']
    # data_listjacketstyle = ['3-in-1 Jacket', 'Anorak', 'Biker', 'Bomber Jacket', 'Military Jacket', 'Motorcycle Jacket', 'Overcoat', 'Parka',
    #             'Pea Coat', 'Puffer Jacket', 'Quilted', 'Rain Coat', 'Trench Coat', 'Varsity Jacket', 'Windbreaker']
    # data_listinsulation = ['Down', 'Polyester', 'Synthetic', 'Wool']
    # data_list = ['1/2 Zip', '1/4 Zip', 'Adjustable', 'All Seasons', 'Belted', 'Breathable', 'Buckle', 'Collarless', 'Full Zip',
    #             'Graphic Print', 'Heavyweight', 'Hooded', 'Insulated', 'Lightweight', 'Lined', 'Moisture Wicking', 'Open', 'Oversized',
    #             'Pockets', 'Preshrunk', 'Reflective', 'Reversible', 'Ring Spun', 'Sheer', 'Shoulder Pads', 'Stretch', 'Tagless', 'Taped Seams',
    #             'Thermal', 'Waterproof', 'Water Resistant']
    data_list = ['14 in', '14.5 in', '15 in', '15.5 in', '16 in', '16.5 in', '17 in', '17.5 in', '18 in', '18.5 in', '19 in', '19.5 in',
                 '20 in', '22 in', '22.5', '23 in']

    for data in data_list:
        code = '&Neck%2520Size=' + data.replace('/', '%252F').replace(' & ', '%2520%2526%2520').replace(' ', '%2520').replace('-', '%252D')
        MensShirtNecksize.objects.create(name=data, code=code)
        print(f'{data} added')

    print("all done")

    # send_mail(
    #     'This is subject Line',
    #     'A message to test with',
    #     'mikem@myfishbay.com',
    #     ['mikemabe@att.net'],
    #     fail_silently=False,
    # )
    # print("done")
    return render(request, 'searchprofile/jayplay.html')
