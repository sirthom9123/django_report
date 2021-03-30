from django.urls import path

from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('list/', views.SaleListView.as_view(), name='list'),
    path('sales/<pk>/', views.SaleDetailView.as_view(), name='detail'),
]
