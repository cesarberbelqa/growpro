from django.urls import path
from . import views

app_name = 'environment'

urlpatterns = [
    path('', views.EnvironmentListView.as_view(), name='list'),
    path('new/', views.EnvironmentCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.EnvironmentUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.EnvironmentDeleteView.as_view(), name='delete'),
]