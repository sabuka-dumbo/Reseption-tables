from django.shortcuts import render
from .models import *

def reception_table(request):
    rooms = Room.objects.all()
    return render(request, 'index.html', {
        'rooms': rooms
    })