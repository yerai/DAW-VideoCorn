from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
     path('<pk>', views.movie, name='movie'),
     path('users/', views.users, name='users'),
]