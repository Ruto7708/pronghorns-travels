from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/', views.booking, name='booking'),
    path('about/', views.about, name='about'),
    path('contactus/', views.contactus, name='contactus'),
    path('pricing/', views.pricing, name='pricing'),
    path('paywithmpesa/', views.paywithmpesa, name='paywithmpesa'),
    path('get-fare/', views.get_fare, name='get_fare'),
    path('api/initiate-payment/', views.initiate_mpesa_payment, name='initiate-mpesa'),
    
    
]

