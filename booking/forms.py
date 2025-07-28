from django import forms
from .models import Booking
from .county_data import COUNTIES

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

    from_county = forms.ChoiceField(choices=[(c, c) for c in COUNTIES])
    to_county = forms.ChoiceField(choices=[(c, c) for c in COUNTIES])
    category = forms.ChoiceField(choices=Booking.CATEGORY_CHOICES, widget=forms.RadioSelect)

    departure_date = forms.DateField(widget=forms.DateInput(attrs={
    'type': 'date',
    'class': 'form-control'
}), label="Departure Date")

departure_time = forms.TimeField(widget=forms.TimeInput(attrs={
    'type': 'time',
    'class': 'form-control'
}), label="Departure Time")

PAYMENT_METHODS = [
    ('mpesa', 'Mpesa'),
]
widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

   