from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '')

register = template.Library()

@register.filter
def get_booking_for_day(booking_groups, day):
    """Find which booking group a specific day belongs to"""
    for booking in booking_groups:
        if booking['start'] <= day <= booking['end']:
            return booking
    return None