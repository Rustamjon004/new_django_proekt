
from  django.urls import path
from online_shop import views

urlpatterns = [

    path('online_shop/', views.product_list, name = 'product_list'),
]