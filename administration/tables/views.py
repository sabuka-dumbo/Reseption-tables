from django.shortcuts import render
from .models import *
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

def index(request):
    rooms = Room.objects.prefetch_related('booking_set').all()
    days = range(1, 32)  # Days 1-31 for August
    return render(request, 'index.html', {
        'rooms': rooms,
        'days': days
    })

def delete_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        # Logic to delete the booking

    return render(request, 'delete.html')

@csrf_exempt
def get_bookings(request):
    if request.method == "POST":
        try:
            json.loads(request.body)

            bookings = [
                {
                    "id": b.id,
                    "guest_name": b.guest_name,
                    "check_in_date": b.check_in_date.isoformat(),
                    "check_out_date": b.check_out_date.isoformat(),
                    "room": {
                        "id": b.room.id,
                        "room_number": b.room.room_number
                    }
                }
                for b in Booking.objects.select_related("room")
            ]

            return JsonResponse({"bookings": bookings})
        except json.JSONDecodeError as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST allowed"}, status=405)