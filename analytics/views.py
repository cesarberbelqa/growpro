from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from plants.models import Plant
from environment.models import Environment
from watering.models import WateringSchedule 

@login_required
def dashboard_view(request):
    user = request.user
    
    total_plants = Plant.objects.filter(user=user, status='Ativa').count()
    total_environments = Environment.objects.filter(user=user).count()
    total_waterings = WateringSchedule .objects.filter(planta__user=user).count()
    
    plants_by_stage = Plant.objects.filter(user=user, status='Ativa') \
                                   .values('estagio_atual__tipo_estagio') \
                                   .annotate(count=Count('id')) \
                                   .order_by('-count')

    context = {
        'total_plants': total_plants,
        'total_environments': total_environments,
        'total_waterings': total_waterings,
        'plants_by_stage': plants_by_stage,
    }
    # Aqui você passaria os dados para um gráfico JS como Chart.js
    return render(request, 'analytics/dashboard.html', context)