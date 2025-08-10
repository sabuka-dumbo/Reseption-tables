from django.db import models

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"Room {self.room_number}"

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    guest_name = models.CharField(max_length=100)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"{self.guest_name} in {self.room} from {self.check_in} to {self.check_out}"
