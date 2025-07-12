from django.contrib import admin
from .models import Environment

@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    search_fields = ['nome', 'localizacao', 'user__email']
    list_display = ('nome', 'user', 'area', 'numero_maximo_plantas', 'estagio_preparado')
    list_filter = ('user', 'estagio_preparado')
    autocomplete_fields = ['user', 'estagio_preparado']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)