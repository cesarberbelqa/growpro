from django.contrib import admin
from .models import Fertilizer

@admin.register(Fertilizer)
class FertilizerAdmin(admin.ModelAdmin):
    search_fields = ['nome', 'tipo', 'user__email']
    list_display = ('nome', 'tipo', 'user')
    list_filter = ('tipo', 'user')
    autocomplete_fields = ['user']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)