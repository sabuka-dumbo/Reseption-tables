from django.shortcuts import render
import calendar
from datetime import date
from collections import defaultdict
from .models import Room, Booking

def reception_table(request):
    year = 2025
    month = 8
    num_days = calendar.monthrange(year, month)[1]
    days = list(range(1, num_days + 1))

    # Get all rooms ordered by room_number
    rooms = Room.objects.order_by('room_number')

    # Prepare bookings grouped by room_number for the month
    bookings_by_room = defaultdict(list)

    # Filter bookings that overlap with the month (simple filter)
    all_bookings = Booking.objects.filter(
        check_in__year=year, check_in__month=month
    ).order_by('check_in')

    for b in all_bookings:
        start_day = b.check_in.day
        end_day = b.check_out.day
        length = end_day - start_day + 1
        bookings_by_room[b.room.room_number].append({
            'start': start_day,
            'length': length,
            'guest_name': b.guest_name,
        })

    # Build table cells: for each room, a list of length num_days for the days in the month
    room_cells = {}

    for room in rooms:
        cells = [''] * num_days  # empty string = free day
        bookings = bookings_by_room.get(room.room_number, [])

        for b in bookings:
            start_idx = b['start'] - 1
            length = b['length']

            # Place booking info at the start day
            cells[start_idx] = {'guest_name': b['guest_name'], 'length': length}

            # Mark covered days as None to skip rendering
            for i in range(start_idx + 1, start_idx + length):
                if i < num_days:
                    cells[i] = None

        room_cells[room.room_number] = cells

    context = {
        'year': year,
        'month': month,
        'days': days,
        'rooms': rooms,
        'room_cells': room_cells,
    }

    return render(request, 'reception_table.html', context)
