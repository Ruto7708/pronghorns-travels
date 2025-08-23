
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

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from .forms import BookingForm
from .models import Booking
from .fare_data import county_distances, FARE_PER_KM   # assuming you have fare logic here

def booking(request):
    booking_instance = None  # store the new booking
    
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

            # ✅ Calculate fare
            distance = county_distances.get(from_county, {}).get(to_county, 0)
            fare = distance * FARE_PER_KM

            if booking_instance.category == "Passenger" and booking_instance.num_passengers > 1:
                fare *= booking_instance.num_passengers

            booking_instance.To_Pay_KES = fare  

            booking_instance.save()

            # Handle file upload (optional)
            uploaded_file = request.FILES.get('file_field')
            if uploaded_file:
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name, uploaded_file)
                file_url = fs.url(filename)
            else:
                file_url = ""

            # ✅ Instead of redirect → render same page with booking info
            return render(request, 'booking.html', {
                'form': BookingForm(),   # empty form for new bookings
                'booking': booking_instance,  # pass booking for receipt
                'file_url': file_url
            })

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




# views.py
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.shortcuts import get_object_or_404
import os
from .models import Booking

def build_ticket_section(booking, copy_type="Passenger Copy"):
    """Build one half of the ticket (company or passenger copy)."""
    styles = getSampleStyleSheet()
    section = []

    # Title
    title = Paragraph(f"<b>Pronghorn Travels - Booking Ticket ({copy_type})</b>", styles["Heading2"])
    section.append(title)
    section.append(Spacer(1, 12))

    # Booking details
    data = [
        ["Booking ID", booking.id],
        ["Full Name", booking.full_name],
        ["Phone Number", booking.phone_number],
        ["Email", booking.email or "-"],
        ["Category", booking.category],
        ["Car Type", booking.car_type],
        ["From", booking.from_county],
        ["To", booking.to_county],
        ["Passengers", booking.num_passengers or "-"],
        ["Parcel Weight", booking.parcel_weight or "-"],
        ["Total Fare", f"KES {booking.To_Pay_KES}"],
        ["Date", booking.created_at.strftime("%d %b %Y %H:%M")],
    ]

    table = Table(data, colWidths=[150, 250])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3498db")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
    ]))
    section.append(table)
    section.append(Spacer(1, 15))

    # Footer
    footer = Paragraph(
        "<i>Thank you for choosing Pronghorn Travels. Have a safe journey!</i>",
        styles["Normal"]
    )
    section.append(footer)

    return section


def download_receipt(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Response settings
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="ticket_{booking.id}.pdf"'

    # Document setup
    doc = SimpleDocTemplate(response, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=40)

    story = []

    # Company Logo (if exists)
    logo_path = os.path.join("static", "images", "logoo.png")
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=100, height=60))
        story.append(Spacer(1, 12))

    # Build two ticket sections
    story.extend(build_ticket_section(booking, "Company Copy"))

    # Add dotted cut line
    cutline = Paragraph(
        '<para alignment="center">------------------------------------- '
        '✂ CUT HERE ✂ '
        '-------------------------------------</para>',
        getSampleStyleSheet()["Normal"]
    )
    story.append(Spacer(1, 20))
    story.append(cutline)
    story.append(Spacer(1, 20))

    story.extend(build_ticket_section(booking, "Passenger Copy"))

    # Build document
    doc.build(story)
    return response



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
