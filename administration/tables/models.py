from django.db import models
from django.utils import timezone

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=50, blank=True, null=True)  # Added room type
    capacity = models.PositiveIntegerField(default=1)  # Added capacity
    
    def __str__(self):
        return f"Room {self.room_number}"

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('confirmed', 'Confirmed'),
        ('checked-in', 'Checked In'),
        ('checked-out', 'Checked Out'),
        ('cancelled', 'Cancelled')
    ], default='confirmed')
    
    def __str__(self):
        return f"Booking for {self.guest_name} in {self.room}"
    
    def is_active_on_date(self, date):
        """Check if booking is active on a specific date"""
        return self.check_in_date <= date <= self.check_out_date