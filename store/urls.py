from django.urls import path
from store import views


urlpatterns = [
    path('', views.store, name='store-home'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search_product, name='search-product'),
]
