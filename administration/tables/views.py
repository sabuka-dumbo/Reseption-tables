from django.shortcuts import render
from .models import *
import json
from django.http import JsonResponse, HttpResponseBadRequest

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


def items_api(request):
    if request.method == "GET":
        bookings = Booking.objects.all()
        return JsonResponse({"items": bookings})

    try:
        data = json.loads(request.body.decode("utf-8"))
        name = data.get("name", "").strip()
        description = data.get("description", "").strip()
        if not name:
            return HttpResponseBadRequest("Missing 'name'")
        item = Item.objects.create(name=name, description=description)
        return JsonResponse({"item": item.to_dict()}, status=201)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")