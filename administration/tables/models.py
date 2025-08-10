from django.db import models
from django.utils import timezone

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"Room {self.room_number})"
