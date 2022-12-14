"""shorturl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from app import views
from app import rest_api

urlpatterns = [
    # Sitio web.
    path('', views.indexView, name='Index'),
    path('index/', views.indexView, name='Index'),
    path('login/', views.loginView, name='Login form'),
    path('auth/', views.authView, name='Authenticate user'),
    path('logout/', views.logoutView, name='Logout user'),
    path('sign-up/', views.signUpView, name='Sign up user'),
    path('register/', views.registerView, name='Register new user'),
    path('my-urls/', views.myURLSView, name='See created URLs'),
    path('<str:short_url>', views.redirectView, name='Redirect to long URL'),
    # Rest-API.
    path('api/', rest_api.makeURL, name='Rest-API'),
    path('api/<int:id>', rest_api.editURL, name='Rest-API'),
]
