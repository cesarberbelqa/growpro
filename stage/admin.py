from django.contrib import admin
from .models import Stage

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    search_fields = ['tipo_estagio']
    list_display = ('tipo_estagio', 'duracao_em_dias', 'luz_diaria_em_horas')
    list_filter = ()
    autocomplete_fields = []