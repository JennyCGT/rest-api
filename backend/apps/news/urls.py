from django.urls import path
from .views import CreateNews, UpdateLike
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('news/', CreateNews.as_view()),
    path('news/like/<int:pk>/',UpdateLike.as_view())    
]