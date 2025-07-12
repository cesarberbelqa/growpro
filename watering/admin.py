from django.contrib import admin
from .models import WateringSchedule

@admin.register(WateringSchedule)
class WateringScheduleAdmin(admin.ModelAdmin):
    list_display = ('planta', 'user', 'frequencia', 'display_proxima_rega', 'is_active')
    list_filter = ('is_active', 'frequencia', 'user')
    search_fields = ('planta__nome', 'planta__identificacao', 'user__email')
    autocomplete_fields = ['planta', 'user']
    list_editable = ('is_active',)

    fieldsets = (
        (None, {
            'fields': ('user', 'planta', 'is_active')
        }),
        ('Detalhes do Agendamento', {
            'fields': ('frequencia', 'dias_intervalo', 'quantidade_agua_ml', 'fertilizantes', 'horario_preferencial')
        }),
        ('Controle de Datas', {
            'fields': ('ultima_rega_registrada',)
        }),
    )

    def display_proxima_rega(self, obj):
        if obj.proxima_rega:
            return obj.proxima_rega.strftime('%d/%m/%Y')
        return "Inativo"
    display_proxima_rega.short_description = "Próxima Rega"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)