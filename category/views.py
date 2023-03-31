from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category
from .forms import CategoryAddNodeForm


def category_list(request):
    return render(request, 'category/list.html', {'categories': Category.objects.all()})


def category_add_root(request):
    if request.method == 'POST':
        form = CategoryAddNodeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Category.objects.create(name=cd['name'], code=cd['code'])

            return redirect('category:category_list')
        else:
            messages.error(request, "Not Valid")
    else:
        form = CategoryAddNodeForm()
        messages.info(request, "No Post")
    return render(request, 'category/add_root_node.html', {'form': form})


def category_add_child(request, parent_id=0):
    if request.method == 'POST':
        form = CategoryAddNodeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            parent_node = Category.objects.get(pk=cd['parent_id'])
            Category.objects.create(name=cd['name'], code=cd['code'], parent=parent_node)
            messages.info(request, parent_node.name)
            return redirect('category:category_list')
        else:
            messages.error(request, "Not Valid")
    else:
        form = CategoryAddNodeForm(initial={'parent_id': parent_id})
        messages.info(request, "No Post")
    return render(request, 'category/add_child_node.html', {'form': form})
