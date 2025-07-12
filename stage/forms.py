from django import forms
from .models import Stage

class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        # O campo 'user' é preenchido automaticamente na view
        fields = [
            'tipo_estagio', 'duracao_em_dias', 'luz_diaria_em_horas',
            'ppfd', 'umidade_recomendada', 'temperatura_recomendada'
        ]
        widgets = {
            'duracao_em_dias': forms.NumberInput(attrs={'min': 1}),
            'luz_diaria_em_horas': forms.NumberInput(attrs={'min': 0, 'max': 24}),
            'ppfd': forms.NumberInput(attrs={'min': 0}),
        }