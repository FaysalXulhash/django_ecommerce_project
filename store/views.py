from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        total_product = products.count()
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        total_product = products.count()
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

    context = {
        #'products': products,
        'total_product': total_product,
        'products': paged_products,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()

    except Exception as e:
        raise e
    context = {
        'product': product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product-detail.html', context)


def search_product(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('created_at').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            total_product = products.count()
            context = {
                'products': products,
                'total_product': total_product,
            }
        else:
            context = {
                'products': [],
                'total_product': 0,
            }
    return render(request, 'store/store.html', context)
