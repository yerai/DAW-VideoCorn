from django.urls import path
from . import views

urlpatterns = [
     path('home/', views.home, name='home'),
     path('home/<pk>', views.movie, name='movie'),
     path('users/', views.users, name='users'),
     path('movies/', views.movies, name='movies'),
     path('log_in/', views.log_in, name='log_in'),
     path('log_out/', views.log_out, name='log_out')
]