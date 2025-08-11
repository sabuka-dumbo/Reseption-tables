from django.shortcuts import render
from .models import *

def index(request):
    rooms = Room.objects.prefetch_related('booking_set').all()
    days = range(1, 32)  # Days 1-31 for August
    return render(request, 'index.html', {
        'rooms': rooms,
        'days': days
    })

def delete_booking(request):
    bookings = Booking.objects.all().select_related('room')
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        # Logic to delete the booking

    return render(request, 'delete.html', {'bookings': bookings})