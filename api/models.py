from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser
    """
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Movie(models.Model):
    """
    Model for storing movie information
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=255)
    cast = models.TextField()  # Stored as comma-separated values
    duration = models.CharField(max_length=20)  # e.g., "2h 30m"
    poster_image = models.URLField(max_length=255, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Showtime(models.Model):
    """
    Model for movie showtimes
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    date = models.DateField()
    time = models.TimeField()
    capacity = models.PositiveIntegerField(default=60)  # Total number of seats
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('movie', 'date', 'time')

    def __str__(self):
        return f"{self.movie.title} - {self.date} {self.time}"
    
    @property
    def reserved_seats(self):
        """
        Calculate the number of reserved seats for this showtime
        """
        return self.reservations.aggregate(
            total_tickets=models.Sum('ticket_count')
        )['total_tickets'] or 0
    
    @property
    def available_seats(self):
        """
        Calculate the number of available seats for this showtime
        """
        return self.capacity - self.reserved_seats

class Reservation(models.Model):
    """
    Model for ticket reservations
    """
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='reservations')
    ticket_count = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.showtime} - {self.ticket_count} tickets"

class Rating(models.Model):
    """
    Model for movie ratings
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')  # One rating per user per movie

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - {self.score} stars"