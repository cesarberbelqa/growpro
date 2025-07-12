from django.contrib import admin
from .models import Plant

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    # O search_fields é o requisito principal para o autocomplete funcionar
    search_fields = ['nome', 'identificacao', 'user__email'] 
    
    list_display = ('nome', 'identificacao', 'user', 'estagio_atual', 'ambiente_atual', 'status')
    list_filter = ('status', 'estagio_atual', 'user')
    autocomplete_fields = ['user', 'estagio_atual', 'ambiente_atual']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)