from django.shortcuts import render
from searchprofile.models import SearchProfile
from django.contrib.auth.decorators import login_required


# @login_required()
# def brand_profile_list(request):
#     profiles = Brand.objects.filter(user=request.user)
#     return render(request, 'brandprofile/brandprofilelist.html', {'profiles': profiles})


# @login_required()
# def brand_profile_detail(request, brand_id):
#     brand = Brand.objects.get(pk=brand_id)
#     profiles = SearchProfile.objects.filter(brand=brand).prefetch_related('results__spec_line')
#     return render(request, 'brandprofile/brandprofiledetail.html', {'brand_name': brand.name, 'profiles': profiles})
