from django.urls import path
from orders import views


urlpatterns = [
    path('place-order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
]