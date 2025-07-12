from django.contrib import admin
from .models import Stage

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    search_fields = ['tipo_estagio', 'user__email']
    list_display = ('tipo_estagio', 'user', 'duracao_em_dias', 'luz_diaria_em_horas')
    list_filter = ('user',)
    autocomplete_fields = ['user']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)