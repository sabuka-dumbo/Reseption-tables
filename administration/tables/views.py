from django.shortcuts import render, redirect
from .models import *
import json
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

def index(request):
    rooms = Room.objects.prefetch_related('booking_set').all()
    days = range(1, 32)  # Days 1-31 for August
    return render(request, 'index.html', {
        'rooms': rooms,
        'days': days
    })

def delete_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('bookings')
        who_deleted = request.POST.get('who_deleted')

        booking = Booking.objects.filter(id=booking_id).first()

        DeletedBookings.objects.create(
            room=booking.room,
            guest_name=booking.guest_name,
            check_in_date=booking.check_in_date,
            check_out_date=booking.check_out_date,
            deleted_by=who_deleted,
            deleted_at=timezone.now()
        )

        booking.delete()

        return redirect('index')

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

def add_booking(request):
    if request.method == 'POST':
        room_id = request.POST.get('room-id')
        room2 = Room.objects.get(id=room_id)
        guest_name = request.POST.get('guest_name')
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        added_by = request.POST.get('who_added')

        try:
            check_in = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_date, '%Y-%m-%d').date()
        except ValueError:
            return redirect('index')

        overlapping = Booking.objects.filter(
            room=room2,
            check_in_date__lt=check_out,
            check_out_date__gt=check_in
        )

        if overlapping.exists():
            # Redirect with error flag in URL query params
            return redirect('/?error=notavailable')

        Booking.objects.create(
            room=room2,
            guest_name=guest_name,
            check_in_date=check_in,
            check_out_date=check_out
        )
        AddedBookings.objects.create(
            room=room2,
            guest_name=guest_name,
            check_in_date=check_in,
            check_out_date=check_out,
            added_by=added_by,
            added_at=timezone.now()
        )
        return redirect('index')

    return render(request, 'add.html')

@csrf_exempt
def get_rooms(request):
    if request.method == "POST":
        try:
            rooms = list(Room.objects.all().values('id', 'room_number'))
            return JsonResponse({"rooms": rooms})
        except json.JSONDecodeError as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST allowed"}, status=405)