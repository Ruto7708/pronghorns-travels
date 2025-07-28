from django.contrib import admin
from .models import ContactMessage, Booking

# Register your models here.


admin.site.register(ContactMessage)
admin.site.register(Booking)



# Admin Panel Branding for Pronghorns Travels
admin.site.site_header = "Pronghorns Travels Admin"
admin.site.site_title = "Pronghorns Admin Portal"
admin.site.index_title = "Welcome to Pronghorns Travels Admin Dashboard"
