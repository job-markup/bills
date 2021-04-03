from django.urls import path

from . import views


app_name = 'products'


urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('stock-alerts/', views.stock_alerts_view, name='alerts'),
    path('<str:slug>/', views.ProductCategory.as_view(),
         name='product_list_by_category'),
]
