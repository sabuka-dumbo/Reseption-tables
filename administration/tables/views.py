from django.shortcuts import render
from datetime import datetime, timedelta
from .models import Room

def index(request):
    now = datetime.now()
    current_month = now.strftime("%B %Y")
    
    # Create list of days in month (1-31)
    days = list(range(1, 32))
    
    # Get ALL rooms (including those without bookings)
    all_rooms = Room.objects.all().order_by('room_number')
    
    # Prepare room data
    rooms = []
    for room in all_rooms:
        booked_days = []
        guest_names = {}  # Dictionary to store guest names per day
        
        if room.check_in and room.check_out:
            # Convert to date if they're datetime objects
            check_in = room.check_in.date() if hasattr(room.check_in, 'date') else room.check_in
            check_out = room.check_out.date() if hasattr(room.check_out, 'date') else room.check_out
            
            # Get all days between check_in and check_out
            delta = check_out - check_in
            for i in range(delta.days + 1):
                day = (check_in + timedelta(days=i)).day
                if day <= 31:  # Only include days that exist in our table
                    booked_days.append(day)
                    guest_names[day] = room.guest_name
        
        rooms.append({
            'room_number': room.room_number,
            'booked_days': booked_days,
            'guest_names': guest_names  # Dictionary of day: guest_name
        })
    
    context = {
        'current_month': current_month,
        'days': days,
        'rooms': rooms,
        'today': now.day  # Pass current day for highlighting
    }
    
    return render(request, 'index.html', context)