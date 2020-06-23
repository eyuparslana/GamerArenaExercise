from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('sign-up/', views.CreateUserView.as_view(), name='signup'),
    path('', include('rest_auth.urls')),
    path('me/', views.UserProfileView.as_view(), name='profile'),
    path('search/', views.ListUsersView.as_view(), name='search')
]
