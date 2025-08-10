from django.db import models
import datetime

# Create your models here.
class Room(models.Model):
    room_number = models.CharField(max_length=10, default='')
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    guest_name = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"Room {self.room_number} ({self.guest_name})"