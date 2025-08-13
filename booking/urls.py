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
    path('success/', views.success, name='success'),
    path('success/<int:booking_id>/', views.success_with_receipt, name='success_with_receipt'),
    path('download-receipt/<int:booking_id>/', views.download_receipt, name='download_receipt'),
    
    
]

