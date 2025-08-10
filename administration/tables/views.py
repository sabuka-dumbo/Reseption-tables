from django.shortcuts import render
from .models import Room, Booking
from datetime import date, timedelta
import calendar

def reception_table(request):
    # Get current month and year or from request parameters
    year = request.GET.get('year', date.today().year)
    month = request.GET.get('month', date.today().month)
    
    try:
        year = int(year)
        month = int(month)
    except (ValueError, TypeError):
        year = date.today().year
        month = date.today().month
    
    # Get all rooms
    rooms = Room.objects.all().order_by('room_number')
    
    # Get all bookings for the month
    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])
    bookings = Booking.objects.filter(
        check_in_date__lte=last_day,
        check_out_date__gte=first_day
    )
    
    # Generate days in month
    num_days = calendar.monthrange(year, month)[1]
    days_in_month = [date(year, month, day) for day in range(1, num_days + 1)]
    
    # Prepare context
    context = {
        'rooms': rooms,
        'bookings': bookings,
        'days_in_month': days_in_month,
        'month_name': first_day.strftime('%B'),
        'year': year,
        'prev_month': (first_day - timedelta(days=1)).month,
        'prev_year': (first_day - timedelta(days=1)).year,
        'next_month': (last_day + timedelta(days=1)).month,
        'next_year': (last_day + timedelta(days=1)).year,
    }
    
    return render(request, 'reception/table.html', context)