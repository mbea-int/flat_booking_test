from django.db import models

# Create your models here.
class Flat(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Booking(models.Model):
    flat = models.ForeignKey(Flat, related_name="bookings", on_delete=models.CASCADE)
    checkin = models.DateField()
    checkout = models.DateField()

    def __str__(self):
        return '%s: %s' % (self.checkin, self.checkout)