from django.shortcuts import render
from datetime import datetime, timedelta
from .models import Room

def index(request):
    # Get current month name and year
    now = datetime.now()
    current_month = now.strftime("%B %Y")
    
    # Create list of days in month (1-31)
    days = list(range(1, 32))
    
    # Get all rooms (ordered by room number)
    all_rooms = Room.objects.all().order_by('room_number')
    
    # Prepare room data
    rooms = []
    for room in all_rooms:
        booked_days = []
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
        
        rooms.append({
            'room_number': room.room_number,
            'guest_name': room.guest_name or "",  # Handle empty guest names
            'booked_days': booked_days
        })
    
    context = {
        'current_month': current_month,
        'days': days,
        'rooms': rooms,
    }
    
    return render(request, 'index.html', context)