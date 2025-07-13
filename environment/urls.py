from django.urls import path
from . import views
from .views import environment_capacity_api

app_name = 'environment'

urlpatterns = [
    path('', views.EnvironmentListView.as_view(), name='list'),
    path('new/', views.EnvironmentCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.EnvironmentUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.EnvironmentDeleteView.as_view(), name='delete'),
    path('api/capacity/<int:pk>/', environment_capacity_api, name='api_capacity'),
]