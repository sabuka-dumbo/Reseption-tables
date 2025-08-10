from django.shortcuts import render
from .models import *

def index(request):
    rooms = Room.objects.all().prefetch_related('booking_set')
    return render(request, 'index.html', {
        'rooms': rooms,
        'days': range(1, 32)
    })