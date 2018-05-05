"""DAWProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('videocorn/', include('videocorn.urls')), 
    path('login/', views.login, {'template_name': 'login.html'}, name='login'),
    path('logout/', views.login, {'template_name': 'login.html'}, name='logout'),
]

# Redirect the base URL to the videocorn application
urlpatterns += [
    path('', RedirectView.as_view(url='/videocorn/')),
]
