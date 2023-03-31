from django.shortcuts import render
from .models import Brand
from searchprofile.models import SearchProfile, ResultSpecs


def brand_profile_list(request):
    return render(request, 'brandprofile/brandprofilelist.html', {'profiles': Brand.objects.all()})


def brand_profile_detail(request, brand_id):
    brand = Brand.objects.get(pk=brand_id)
    profiles = SearchProfile.objects.filter(brand=brand).prefetch_related('results__spec_line')
    return render(request, 'brandprofile/brandprofiledetail.html', {'brand_name':brand.name, 'profiles': profiles})
