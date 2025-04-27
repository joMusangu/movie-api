from rest_framework import serializers
from .models import User, Movie, Showtime, Reservation, Rating
from api import models

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_admin', 'date_joined']
        read_only_fields = ['id', 'is_admin', 'date_joined']

# Movie Serializer
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        # In MovieSerializer class Meta
    fields = ['id', 'title', 'description', 'genre', 'director', 'cast', 'duration', 'poster_image', 'average_rating', 'rating_count']

    # Add these methods to MovieSerializer
    def get_average_rating(self, obj):
        return obj.ratings.aggregate(avg=models.Avg('score'))['avg'] or 0

    def get_rating_count(self, obj):
        return obj.ratings.count()

# Showtime Serializer
class ShowtimeSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Showtime
        fields = ['id', 'movie', 'date', 'time', 'capacity', 'reserved_seats', 'available_seats']
        read_only_fields = ['id', 'reserved_seats', 'available_seats']

# Reservation Serializer
class ReservationSerializer(serializers.ModelSerializer):
    showtime = ShowtimeSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'showtime', 'ticket_count', 'total_price', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'total_price', 'status', 'created_at']