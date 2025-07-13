from plants.models import Plant

def plant_context(request):
    """
    Adiciona informações relacionadas a plantas ao contexto global.
    """
    has_plants = False
    if request.user.is_authenticated:
        # Verifica se o usuário logado tem pelo menos uma planta
        has_plants = Plant.objects.filter(user=request.user).exists()
    
    return {
        'user_has_plants': has_plants
    }