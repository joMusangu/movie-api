from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.utils import timezone
from django.db.models import Avg

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

import json
from datetime import datetime

from .models import User, Movie, Showtime, Reservation, Rating
from .serializers import LoginSerializer, MovieSerializer, ReservationSerializer
from api import models


# Authentication views
@csrf_exempt
@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin
        }, status=201)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Movie views
@csrf_exempt
@api_view(['GET', 'POST'])
def movie_list_create(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_update_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        movie.delete()
        return Response({'message': 'Movie deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    data = [{
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'genre': movie.genre,
        'director': movie.director,
        'cast': movie.cast.split(','),
        'duration': movie.duration,
        'poster_image': movie.poster_image,
        'average_rating': movie.ratings.aggregate(avg=Avg('score'))['avg'] or 0,
        'rating_count': movie.ratings.count()
    } for movie in movies]
    
    return Response(data)

@csrf_exempt
@api_view(['GET'])
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    
    # Get showtimes for the movie
    showtimes = movie.showtimes.all()
    showtime_data = [{
        'id': showtime.id,
        'date': showtime.date,
        'time': showtime.time.strftime('%H:%M'),
        'available_seats': showtime.available_seats
    } for showtime in showtimes]
    
    data = {
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'genre': movie.genre,
        'director': movie.director,
        'cast': movie.cast.split(','),
        'duration': movie.duration,
        'poster_image': movie.poster_image,
        'average_rating': movie.ratings.aggregate(avg=Avg('score'))['avg'] or 0,
        'rating_count': movie.ratings.count(),
        'showtimes': showtime_data
    }
    
    return Response(data)

@csrf_exempt
@api_view(['POST'])
def movie_create(request):
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['PUT'])
def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    
    movie.title = request.data.get('title', movie.title)
    movie.description = request.data.get('description', movie.description)
    movie.genre = request.data.get('genre', movie.genre)
    movie.director = request.data.get('director', movie.director)
    
    cast = request.data.get('cast')
    if cast:
        movie.cast = ','.join(cast) if isinstance(cast, list) else cast
    
    movie.duration = request.data.get('duration', movie.duration)
    
    poster_image = request.FILES.get('poster_image')
    if poster_image:
        movie.poster_image = poster_image
    
    movie.save()
    
    return Response({
        'id': movie.id,
        'title': movie.title,
        'message': 'Movie updated successfully'
    })

@csrf_exempt
@api_view(['DELETE'])
def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.delete()
    
    return Response({
        'message': 'Movie deleted successfully'
    })

# Showtime views
@csrf_exempt
@api_view(['GET'])
def showtime_list(request):
    date_str = request.query_params.get('date')
    movie_id = request.query_params.get('movie_id')
    
    showtimes = Showtime.objects.all()
    
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        showtimes = showtimes.filter(date=date)
    
    if movie_id:
        showtimes = showtimes.filter(movie_id=movie_id)
    
    data = [{
        'id': showtime.id,
        'movie': {
            'id': showtime.movie.id,
            'title': showtime.movie.title
        },
        'date': showtime.date,
        'time': showtime.time.strftime('%H:%M'),
        'capacity': showtime.capacity,
        'reserved_seats': showtime.reserved_seats,
        'available_seats': showtime.available_seats
    } for showtime in showtimes]
    
    return Response(data)

@csrf_exempt
@api_view(['POST'])
def showtime_create(request):
    movie_id = request.data.get('movie_id')
    date_str = request.data.get('date')
    time_str = request.data.get('time')
    capacity = request.data.get('capacity', 60)
    
    movie = get_object_or_404(Movie, pk=movie_id)
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    time = datetime.strptime(time_str, '%H:%M').time()
    
    showtime = Showtime.objects.create(
        movie=movie,
        date=date,
        time=time,
        capacity=capacity
    )
    
    return Response({
        'id': showtime.id,
        'movie': movie.title,
        'date': date,
        'time': time.strftime('%H:%M'),
        'message': 'Showtime created successfully'
    }, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['DELETE'])
def showtime_delete(request, pk):
    showtime = get_object_or_404(Showtime, pk=pk)
    showtime.delete()
    
    return Response({
        'message': 'Showtime deleted successfully'
    })

# Reservation views
@csrf_exempt
@api_view(['POST'])
def reservation_create(request):
    showtime_id = request.data.get('showtime_id')
    ticket_count = int(request.data.get('ticket_count', 1))
    
    showtime = get_object_or_404(Showtime, pk=showtime_id)
    
    # Check if there are enough seats available
    if showtime.available_seats < ticket_count:
        return Response({
            'error': 'Not enough seats available'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Calculate total price ($12 per ticket)
    total_price = ticket_count * 12.00
    
    with transaction.atomic():
        reservation = Reservation.objects.create(
            user=request.user,
            showtime=showtime,
            ticket_count=ticket_count,
            total_price=total_price,
            status='upcoming'
        )
    
    return Response({
        'id': reservation.id,
        'movie': showtime.movie.title,
        'date': showtime.date,
        'time': showtime.time.strftime('%H:%M'),
        'ticket_count': ticket_count,
        'total_price': total_price,
        'message': 'Reservation created successfully'
    }, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['DELETE'])
def reservation_cancel(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    
    # Check if the reservation belongs to the user
    if reservation.user != request.user and not request.user.is_admin:
        return Response({
            'error': 'You do not have permission to cancel this reservation'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Check if the reservation is upcoming
    if reservation.status != 'upcoming':
        return Response({
            'error': 'Only upcoming reservations can be cancelled'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    reservation.status = 'cancelled'
    reservation.save()
    
    return Response({
        'message': 'Reservation cancelled successfully'
    })

@api_view(['GET'])
def user_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    data = [{
        'id': reservation.id,
        'movie': {
            'id': reservation.showtime.movie.id,
            'title': reservation.showtime.movie.title,
            'poster_image': request.build_absolute_uri(reservation.showtime.movie.poster_image.url) if reservation.showtime.movie.poster_image else None
        },
        'showtime': {
            'date': reservation.showtime.date,
            'time': reservation.showtime.time.strftime('%H:%M')
        },
        'ticket_count': reservation.ticket_count,
        'total_price': float(reservation.total_price),
        'status': reservation.status,
        'created_at': reservation.created_at
    } for reservation in reservations]
    
    return Response(data)

@api_view(['GET', 'POST'])
def reservation_list_create(request):
    if request.method == 'GET':
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def reservation_detail_cancel(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    if request.method == 'GET':
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if reservation.user != request.user and not request.user.is_admin:
            return Response({'error': 'You do not have permission to cancel this reservation'}, status=status.HTTP_403_FORBIDDEN)
        reservation.status = 'cancelled'
        reservation.save()
        return Response({'message': 'Reservation cancelled successfully'})

# Admin views
@api_view(['GET'])
def admin_dashboard(request):
    # Get counts
    movie_count = Movie.objects.count()
    user_count = User.objects.count()
    
    # Today's reservations
    today = timezone.now().date()
    today_reservations = Reservation.objects.filter(
        showtime__date=today,
        status='upcoming'
    ).count()
    
    # Weekly revenue
    week_start = today - timezone.timedelta(days=today.weekday())
    week_end = week_start + timezone.timedelta(days=6)
    weekly_revenue = Reservation.objects.filter(
        created_at__date__range=[week_start, week_end]
    ).aggregate(total=models.Sum('total_price'))['total'] or 0
    
    return Response({
        'movie_count': movie_count,
        'user_count': user_count,
        'today_reservations': today_reservations,
        'weekly_revenue': float(weekly_revenue)
    })

@api_view(['POST'])
def promote_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_admin = True
    user.save()
    
    return Response({
        'message': f'User {user.username} promoted to admin successfully'
    })

@api_view(['POST'])
def demote_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # Prevent demoting yourself
    if user == request.user:
        return Response({
            'error': 'You cannot demote yourself'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user.is_admin = False
    user.save()
    
    return Response({
        'message': f'User {user.username} demoted from admin successfully'
    })

@api_view(['GET'])
@permission_classes([AllowAny])  # Allow unrestricted access
def current_user(request):
    """
    Return the authenticated user's details
    """
    user = request.user if request.user.is_authenticated else None
    if user:
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_admin': user.is_admin,
            'date_joined': user.date_joined
        })
    else:
        return Response({'error': 'No authenticated user'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'PUT'])
def user_profile(request):
    """
    Get or update the authenticated user's profile
    """
    user = request.user
    
    if request.method == 'GET':
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_admin': user.is_admin,
            'date_joined': user.date_joined
        })
    
    elif request.method == 'PUT':
        # Update user profile
        data = request.data
        
        # Update fields if provided
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            # Check if email is already taken by another user
            if User.objects.exclude(pk=user.pk).filter(email=data['email']).exists():
                return Response({'error': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)
            user.email = data['email']
            
        # Handle password change if provided
        if 'current_password' in data and 'new_password' in data:
            if not user.check_password(data['current_password']):
                return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(data['new_password'])
        
        user.save()
        
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_admin': user.is_admin,
            'message': 'Profile updated successfully'
        })
    
@api_view(['GET', 'POST', 'PUT'])
def movie_ratings(request, pk):
    """
    Get all ratings for a movie or create/update a rating
    """
    movie = get_object_or_404(Movie, pk=pk)
    
    if request.method == 'GET':
        # Get all ratings for the movie
        ratings = Rating.objects.filter(movie=movie).order_by('-created_at')
        
        # Calculate average rating
        average_rating = ratings.aggregate(avg=Avg('score'))['avg'] or 0
        
        # Format ratings for response
        ratings_data = [{
            'id': rating.id,
            'user': {
                'id': rating.user.id if rating.user else None,
                'username': rating.user.username if rating.user else "Anonymous"
            },
            'score': rating.score,
            'comment': rating.comment,
            'created_at': rating.created_at
        } for rating in ratings]
        
        return Response({
            'average_rating': average_rating,
            'rating_count': ratings.count(),
            'ratings': ratings_data
        })
    
    elif request.method in ['POST', 'PUT']:
        score = request.data.get('score')
        comment = request.data.get('comment', '')
        
        if not score or not (1 <= int(score) <= 5):
            return Response({'error': 'Rating must be between 1 and 5'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Allow anonymous users to submit ratings
        user = request.user if request.user.is_authenticated else None
        
        # Update or create rating
        rating, created = Rating.objects.update_or_create(
            user=user,  # Explicitly set to None for anonymous users
            movie=movie,
            defaults={
                'score': score,
                'comment': comment
            }
        )
        
        return Response({
            'id': rating.id,
            'score': rating.score,
            'comment': rating.comment,
            'created_at': rating.created_at,
            'message': 'Rating submitted successfully'
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_movie_rating(request, pk):
    """
    Get the authenticated user's rating for a specific movie
    """
    movie = get_object_or_404(Movie, pk=pk)
    
    try:
        rating = Rating.objects.get(user=request.user, movie=movie)
        return Response({
            'id': rating.id,
            'score': rating.score,
            'comment': rating.comment,
            'created_at': rating.created_at
        })
    except Rating.DoesNotExist:
        return Response({'error': 'Rating not found'}, status=status.HTTP_404_NOT_FOUND)