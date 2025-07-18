from django.urls import path
from . import views

app_name = 'watering'

urlpatterns = [
    path('', views.WateringScheduleListView.as_view(), name='list'),
    path('new/', views.WateringScheduleCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.WateringScheduleUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.WateringScheduleDeleteView.as_view(), name='delete'),
    path('plant/<int:plant_pk>/water/', views.WaterPlantNowView.as_view(), name='water_now'),
    path('<int:pk>/clone/', views.CloneWateringScheduleView.as_view(), name='clone'),
]