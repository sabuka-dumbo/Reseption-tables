from django.db import models
from django.utils import timezone

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"Room {self.room_number})"

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    check_in_date = models.DateField()
    check_out_date = models.DateField()

    def __str__(self):
        return f"Booking for {self.guest_name} in {self.room}"
    
    @property
    def duration(self):
        return (self.check_out_date - self.check_in_date).days + 1

class DeletedBookings(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    deleted_at = models.DateTimeField(auto_now_add=True)
    deleted_by = models.CharField(max_length=150)

    def __str__(self):
        return f"Deleted by {self.deleted_by} on {self.deleted_at}"

class AddedBookings(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default='')
    guest_name = models.CharField(max_length=100)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.CharField(max_length=150)

    def __str__(self):
        return f"Added by {self.added_by} on {self.added_at}"
