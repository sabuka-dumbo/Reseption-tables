from django.shortcuts import render
import calendar
from datetime import datetime
from collections import defaultdict

from .models import Room

def reception_table(request):
    year = 2025
    month = 8
    num_days = calendar.monthrange(year, month)[1]
    days = list(range(1, num_days + 1))

    # Get all unique room numbers
    rooms = Room.objects.values_list('room_number', flat=True).distinct().order_by('room_number')

    # Group bookings by room_number
    bookings_by_room = defaultdict(list)
    for booking in Room.objects.filter(check_in__year=year, check_in__month=month):
        # calculate start and end days clipped to month days
        start_day = max(booking.check_in.day, 1)
        end_day = min(booking.check_out.day, num_days)
        length = end_day - start_day + 1

        bookings_by_room[booking.room_number].append({
            'start': start_day,
            'length': length,
            'guest_name': booking.guest_name,
        })

    # Prepare day cells for each room
    room_cells = {}

    for room_number in rooms:
        cells = [''] * num_days
        bookings = bookings_by_room.get(room_number, [])

        for b in bookings:
            start_idx = b['start'] - 1
            length = b['length']

            # place booking at start
            cells[start_idx] = {'guest_name': b['guest_name'], 'length': length}
            # mark rest as None to skip rendering
            for i in range(start_idx + 1, start_idx + length):
                if i < num_days:
                    cells[i] = None

        room_cells[room_number] = cells

    context = {
        'year': year,
        'month': month,
        'days': days,
        'rooms': rooms,
        'room_cells': room_cells,
    }
    return render(request, 'reception_table.html', context)
