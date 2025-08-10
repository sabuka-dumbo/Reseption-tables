from django.db import models
import datetime

# Create your models here.
class Room(models.Model):
    room_number = models.CharField(max_length=10)
    check_in = models.DateTimeField(default=datetime.datetime.now)
    check_out = models.DateTimeField(default=datetime.datetime.now)
    guest_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Room {self.room_number} ({self.guest_name})"