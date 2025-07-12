from django.urls import path
from . import views

app_name = 'growth_history'

urlpatterns = [
    # URL para criar um novo registro de histórico para uma planta específica
    path('new/', views.GrowthHistoryCreateView.as_view(), name='create'),
    # URL para deletar um registro específico
    path('<int:pk>/delete/', views.GrowthHistoryDeleteView.as_view(), name='delete'),
]