from django.contrib import admin
from .models import Stage, StageTransition

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    search_fields = ['tipo_estagio']
    list_display = ('tipo_estagio', 'duracao_em_dias', 'luz_diaria_em_horas')
    list_filter = ()
    autocomplete_fields = []

@admin.register(StageTransition)
class StageTransitionAdmin(admin.ModelAdmin):
    list_display = ('estagio_atual', 'proximo_estagio')
    autocomplete_fields = ['estagio_atual', 'proximo_estagio']
    list_editable = ('proximo_estagio',)