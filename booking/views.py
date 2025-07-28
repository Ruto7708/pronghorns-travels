
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .utils import lipa_na_mpesa
from .models import ContactMessage
from .forms import BookingForm
from .county_data import DISTANCES
from .models import Booking


# Create your views here.
def home(request):
    return render(request, 'home.html')

RATE_PER_KM = 5

def calculate_fare(from_county, to_county):
    distance = DISTANCES.get((from_county, to_county)) or DISTANCES.get((to_county, from_county))
    return distance * RATE_PER_KM if distance else 0

from django.shortcuts import render
from django.http import JsonResponse
from .forms import BookingForm
from .models import Booking
from .distance_data import county_distances

FARE_PER_KM = 5

def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # You can change this to any page or message
    else:
        form = BookingForm()
    return render(request, 'booking.html', {'form': form})

def get_fare(request):
    from_county = request.GET.get('from')
    to_county = request.GET.get('to')
    category = request.GET.get('category')
    num_passengers = int(request.GET.get('passengers', '1'))

    if from_county and to_county:
        distance = county_distances.get(from_county, {}).get(to_county, 0)
        fare = distance * FARE_PER_KM
        if category == 'Passenger' and num_passengers > 1:
            fare *= num_passengers
        return JsonResponse({'fare': round(fare, 2)})
    return JsonResponse({'fare': 0})

def about(request):
    return render(request, 'about.html')


def contactus(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            phone=phone,
            email=email,
            subject=subject,
            message=message
        )

        return redirect('contactus')  # or show success message

    return render(request, 'contactus.html')

def pricing(request):
    return render(request, 'pricing.html')

def paywithmpesa(request):
    return render(request, 'paywithmpesa.html')



def initiate_mpesa_payment(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')

        if not phone or not amount:
            return JsonResponse({'error': 'Missing phone or amount'}, status=400)

        try:
            response = lipa_na_mpesa(phone, int(amount))
            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
