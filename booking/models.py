from django.db import models
from django.utils import timezone

# Create your models here.


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20) 
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"





class Booking(models.Model):
    CATEGORY_CHOICES = [
        ('Passenger', 'Passenger'),
        ('Parcel', 'Parcel')
    ]

    CAR_CHOICES = [
    ('Bus', 'Bus'),
    ('14 Seater', '14 Seater'),
    ('Wish', 'Wish'),
    ('Noah', 'Noah'),
    ('Voxy', 'Voxy'),
]

    # PAYMENT_METHODS = [
    #     ('mpesa', 'Mpesa'),
    # ]

    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    id_number = models.IntegerField(default=40090973)
    from_county = models.CharField(max_length=100)
    to_county = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    num_passengers = models.PositiveIntegerField(null=True, blank=True)
    parcel_weight = models.FloatField(null=True, blank=True)
    departure_date = models.DateField()
    departure_time = models.TimeField(default=timezone.now) 
    car_type = models.CharField(max_length=20, choices=CAR_CHOICES)
    To_Pay_KES = models.DecimalField(max_digits=10, decimal_places=2)
    # payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    # mpesa_number = models.CharField(max_length=15, blank=True)  # 🔹 New field for Mpesa number
    # payment_code = models.CharField(max_length=50, blank=True)
    
   

    def __str__(self):
        return f"{self.full_name} - {self.category}"
    

