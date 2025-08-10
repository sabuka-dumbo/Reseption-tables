from django.shortcuts import render
from datetime import datetime, timedelta
from .models import Room

def index(request):
    # Get current month name and year
    now = datetime.now()
    current_month = now.strftime("%B %Y")
    
    # Create list of days in month (1-31)
    days = list(range(1, 32))
    
    # Get all rooms and their bookings
    rooms = []
    for room in Room.objects.all():
        # Determine which days this room is booked
        booked_days = []
        if room.check_in and room.check_out:
            # Get all days between check_in and check_out
            delta = room.check_out - room.check_in
            for i in range(delta.days + 1):
                day = (room.check_in + timedelta(days=i)).day
                booked_days.append(day)
        
        rooms.append({
            'room_number': room.room_number,
            'guest_name': room.guest_name,
            'booked_days': booked_days
        })
    
    context = {
        'current_month': current_month,
        'days': days,
        'rooms': rooms,
    }

    return render(request, 'index.html', context)