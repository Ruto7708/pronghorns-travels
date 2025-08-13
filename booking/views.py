
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

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from .forms import BookingForm
from .models import Booking
from .distance_data import county_distances

FARE_PER_KM = 5  # Adjust this rate as needed

def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST, request.FILES)
        if form.is_valid():
            booking_instance = form.save(commit=False)

            # Get form values
            booking_instance.category = request.POST.get('category')
            booking_instance.car_type = request.POST.get('car_type')
            booking_instance.num_passengers = int(request.POST.get('num_passengers') or 1)
            booking_instance.parcel_weight = request.POST.get('parcel_weight') or None

            from_county = request.POST.get('from_county')
            to_county = request.POST.get('to_county')

            # Calculate fare
            distance = county_distances.get(from_county, {}).get(to_county, 0)
            fare = distance * FARE_PER_KM

            if booking_instance.category == "Passenger" and booking_instance.num_passengers > 1:
                fare *= booking_instance.num_passengers

            booking_instance.To_Pay_KES = fare  # ✅ Ensure this is saved so form validates

            booking_instance.save()

            # Handle file upload (optional)
            uploaded_file = request.FILES.get('file_field')
            if uploaded_file:
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name, uploaded_file)
                file_url = fs.url(filename)
            else:
                file_url = ""

            # ✅ Pass booking ID to success page so we can display/download receipt
            return redirect('success_with_receipt', booking_id=booking_instance.id)

        else:
            print("Form errors:", form.errors)
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


def success_with_receipt(request, booking_id):
    """Renders success page with booking details for receipt download"""
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'success.html', {'booking': booking})




import io
from django.http import FileResponse, Http404
from django.template.loader import get_template
from xhtml2pdf import pisa

def download_receipt(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        raise Http404("Booking not found.")

    template = get_template('receipt_template.html')
    html = template.render({'booking': booking})

    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)
    if pisa_status.err:
        return HttpResponse('Error generating receipt', status=500)

    result.seek(0)
    return FileResponse(result, as_attachment=True, filename=f"receipt_{booking.id}.pdf")





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


# from django.shortcuts import render, redirect
# from django.core.files.storage import FileSystemStorage
# from .forms import BookingForm  # your form

# def booking_form(request):
#     if request.method == "POST":
#         form = BookingForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Save the form data
#             instance = form.save()

#             # Optional: Save uploaded file to a known location
#             uploaded_file = request.FILES.get('file_field')  # Replace file_field with your form field name
#             if uploaded_file:
#                 fs = FileSystemStorage()
#                 filename = fs.save(uploaded_file.name, uploaded_file)
#                 file_url = fs.url(filename)
#             else:
#                 file_url = ""

#             # Redirect to success page with file link
#             return render(request, 'success.html', {'file_url': file_url})
#     else:
#         form = BookingForm()

#     return render(request, 'booking_form.html', {'form': form})

def success(request):
    return render(request, 'success.html')
