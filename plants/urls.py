from django.urls import path
from . import views

app_name = 'plants'

urlpatterns = [
    path('', views.PlantListView.as_view(), name='list'),
    path('<int:pk>/', views.PlantDetailView.as_view(), name='detail'),
    path('new/', views.PlantCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.PlantUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.PlantDeleteView.as_view(), name='delete'),
    path('<int:pk>/transition/', views.TransitionStageView.as_view(), name='transition_stage'),
]