from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Movies
    path('movies/', views.movie_list, name='movie-list'),
    path('movies/<int:pk>/', views.movie_detail, name='movie-detail'),
    path('movies/create/', views.movie_create, name='movie-create'),
    path('movies/<int:pk>/update/', views.movie_update, name='movie-update'),
    path('movies/<int:pk>/delete/', views.movie_delete, name='movie-delete'),
    
    # Showtimes
    path('showtimes/', views.showtime_list, name='showtime-list'),
    path('showtimes/create/', views.showtime_create, name='showtime-create'),
    path('showtimes/<int:pk>/delete/', views.showtime_delete, name='showtime-delete'),
    
    # Reservations
    path('reservations/create/', views.reservation_create, name='reservation-create'),
    path('reservations/user/', views.user_reservations, name='user-reservations'),
    path('reservations/<int:pk>/cancel/', views.reservation_cancel, name='reservation-cancel'),
    
    # Admin
    path('admin/dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('admin/users/<int:pk>/promote/', views.promote_user, name='promote-user'),
    path('admin/users/<int:pk>/demote/', views.demote_user, name='demote-user'),

    
    path('user/profile/', views.user_profile, name='user-profile'),
    path('user/current/', views.current_user, name='current-user'),

    # Ratings
    path('movies/<int:pk>/ratings/', views.movie_ratings, name='movie-ratings'),
    path('movies/<int:pk>/ratings/user/', views.user_movie_rating, name='user-movie-rating'),
]
