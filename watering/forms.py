from django import forms
from .models import WateringSchedule
from plants.models import Plant
from fertilizer.models import Fertilizer

class WateringScheduleForm(forms.ModelForm):
    class Meta:
        model = WateringSchedule
        fields = [
            'planta', 'frequencia', 'dias_intervalo', 'quantidade_agua_ml', 
            'fertilizantes', 'horario_preferencial', 'is_active'
        ]
        widgets = {
            'horario_preferencial': forms.TimeInput(attrs={'type': 'time'}),
            'fertilizantes': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        
        # Filtra dropdowns para mostrar apenas itens do usuário
        self.fields['planta'].queryset = Plant.objects.filter(user=user)
        self.fields['fertilizantes'].queryset = Fertilizer.objects.filter(user=user)

        # Se for um formulário de edição, a planta não pode ser alterada
        if self.instance and self.instance.pk:
            self.fields['planta'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        frequencia = cleaned_data.get('frequencia')
        dias_intervalo = cleaned_data.get('dias_intervalo')

        if frequencia == WateringSchedule.FrequenciaChoices.INTERVALO:
            if not dias_intervalo or dias_intervalo < 1:
                self.add_error('dias_intervalo', 'Este campo é obrigatório quando a frequência é "A cada X dias".')
        
        return cleaned_data