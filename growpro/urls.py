from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from plants.views import PlantViewSet

# Configuração do Router para a API
router = DefaultRouter()
router.register(r'plants', PlantViewSet, basename='plant-api')
# Adicione outros viewsets aqui
# router.register(r'environments', EnvironmentViewSet, basename='environment-api')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # URLs dos Apps
    path('accounts/', include('django.contrib.auth.urls')), # Inclui login, logout, etc.
    path('accounts/', include('accounts.urls')),
    path('plants/', include('plants.urls')),
    path('analytics/', include('analytics.urls')),
    path('watering/', include('watering.urls')),
    
    # ADICIONE ESTAS LINHAS
    path('stages/', include('stage.urls')),
    path('environments/', include('environment.urls')),
    # API URLs
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)