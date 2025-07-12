from django.urls import path
from .views import RegisterView, profile_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # ADICIONE A LINHA ABAIXO
    path('profile/', profile_view, name='profile'),
]