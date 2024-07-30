from django.shortcuts import render, redirect
from online_shop.models import Category
def product_list(request):
    return render(request, 'online_shop/home.html')
# Create your views here.

def categories(request):
    category_list = Category.objects.all()
    context = {
        'category_list': category_list

    }
    return render (request,'online_shop/home.hrml',context)
