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
    
    # Prepare room data with booking groups
    rooms = []
    for room in all_rooms:
        # Initialize data structures
        booked_days = []
        guest_names = {}
        booking_groups = []
        current_booking = None
        
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
                    
                    # Track booking groups for continuous display
                    if not current_booking:
                        current_booking = {
                            'start': day,
                            'end': day,
                            'guest': room.guest_name
                        }
                    else:
                        current_booking['end'] = day
            
            # Add the last booking group if it exists
            if current_booking:
                booking_groups.append(current_booking)
        
        rooms.append({
            'room_number': room.room_number,
            'booked_days': booked_days,
            'guest_names': guest_names,
            'booking_groups': booking_groups,
            'current_guest': room.guest_name if booked_days else None
        })
    
    context = {
        'current_month': current_month,
        'days': days,
        'rooms': rooms,
        'today': now.day  # Pass current day for highlighting
    }
    
    return render(request, 'index.html', context)


# Add this custom filter function if you're keeping it in views.py
# (Better practice is to put it in templatetags/custom_filters.py)
def get_booking_for_day(bookings, day):
    """Custom filter to find which booking a day belongs to"""
    for booking in bookings:
        if booking['start'] <= day <= booking['end']:
            return booking
    return None