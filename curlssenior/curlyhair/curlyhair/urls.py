"""
URL configuration for curlyhair project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include  # Add 'include' to include app URLs
from curlyhair import views  # Make sure this is the correct import path
from django.shortcuts import render


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Root URL now points to the home view
    path('quiz/', include('quiz.urls')),  # Include the quiz app URLs here
]
