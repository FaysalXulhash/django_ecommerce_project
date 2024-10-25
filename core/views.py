from django.shortcuts import render
from store.models import Product
from category.models import Category
# Create your views here.


def home(request):
    products = Product.objects.all().filter(is_available = True)
    #categories = Category.objects.all()
    context = {
        'products': products,
        #'categoreis': categories,
    }
    return render(request, 'core/home.html', context)
