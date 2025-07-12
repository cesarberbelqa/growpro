from django.contrib import admin
from .models import GrowthHistory

@admin.register(GrowthHistory)
class GrowthHistoryAdmin(admin.ModelAdmin):
    list_display = ('planta', 'user', 'tipo_evento', 'data_hora_evento')
    list_filter = ('tipo_evento', 'user')
    search_fields = ('planta__nome', 'observacoes', 'user__email')
    autocomplete_fields = ['user', 'planta']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)