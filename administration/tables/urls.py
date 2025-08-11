from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete/', views.delete_booking, name='delete_booking'),
    path('change/', views.change_booking, name='change_booking'),

    ## API
    path('get_bookings/', views.get_bookings, name='get_bookings'),
]