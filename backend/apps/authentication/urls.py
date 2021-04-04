from django.contrib import admin
from django.urls import path
from apps.authentication.views import  LoginViews,  CreateUsersView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('user/login/',LoginViews.as_view() ),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('user/create/', CreateUsersView.as_view())

]
