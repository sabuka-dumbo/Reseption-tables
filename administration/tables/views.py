from django.shortcuts import render
from .models import *

def index(request):
    rooms = Room.objects.all()
    bookings = Booking.objects.filter(
        check_in_date__month=8,  # August
        check_out_date__month=8  # August
    )
    return render(request, 'index.html', {
        'rooms': rooms,
        'bookings': bookings
    })