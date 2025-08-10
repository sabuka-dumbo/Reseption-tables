from django import template

register = template.Library()

@register.filter
def get_booking_for_day(bookings, day):
    for booking in bookings:
        if booking.check_in_date.day <= day <= booking.check_out_date.day:
            return booking
    return None