from django.urls import path
from . import views

app_name = 'stage'

urlpatterns = [
    path('', views.StageListView.as_view(), name='list'),
    path('new/', views.StageCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.StageUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.StageDeleteView.as_view(), name='delete'),
]