from django.db import models
from django.contrib.auth.models import User


class Service(models.Model):
    ICON_CHOICES = [
        ('mind', 'Mind'),
        ('heart', 'Heart'),
        ('family', 'Family'),
        ('teen', 'Teen'),
        ('grief', 'Grief'),
        ('stress', 'Stress'),
        ('trauma', 'Trauma'),
        ('mindfulness', 'Mindfulness'),
        ('career', 'Career'),
        ('group', 'Group'),
    ]

    SESSION_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('couples', 'Couples'),
        ('family', 'Family'),
        ('group', 'Group'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default='mind')
    session_type = models.CharField(max_length=20, choices=SESSION_TYPE_CHOICES, default='individual')

    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Session length in minutes")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    MODE_CHOICES = [
        ('in_person', 'In Person'),
        ('virtual', 'Virtual (Video Call)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    phone = models.CharField(max_length=20)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='in_person')

    date = models.DateField()
    time = models.TimeField()

    notes = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.user.username} - {self.service.name}"

    @property
    def can_cancel(self):
        """A client can only cancel bookings that are still Pending or Confirmed."""
        return self.status in ('Pending', 'Confirmed')
