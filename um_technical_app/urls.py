from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.ServiceListView.as_view(), name='service-list'),
    path('services/preview/', views.ServiceListPreviewView.as_view(), name='service-list-preview'),
  
]

