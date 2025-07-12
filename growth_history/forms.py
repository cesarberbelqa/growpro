from django import forms
from django.utils import timezone 
from .models import GrowthHistory

class GrowthHistoryForm(forms.ModelForm):
    class Meta:
        model = GrowthHistory
        # Os campos 'user' e 'planta' serão preenchidos automaticamente na view
        fields = ['tipo_evento', 'observacoes', 'foto', 'data_hora_evento']
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 4}),
            'data_hora_evento': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializa o campo de data/hora com o valor atual, formatado para o widget
        if not self.instance.pk:
            # Define o valor inicial para o campo com a data e hora atuais.
            # O widget formatará isso automaticamente para 'YYYY-MM-DDTHH:MM'.
            self.fields['data_hora_evento'].initial = timezone.now()