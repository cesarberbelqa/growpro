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

# ==========================================================
#               NOVO FORMULÁRIO PARA CLONAGEM
# ==========================================================
class CloneWateringScheduleForm(forms.Form):
    # Usamos um ModelMultipleChoiceField para permitir a seleção de uma ou mais plantas
    plantas_destino = forms.ModelMultipleChoiceField(
        queryset=Plant.objects.none(), # O queryset será definido na view
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Selecione as plantas para as quais deseja clonar este agendamento"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        agendamento_a_clonar = kwargs.pop('source_schedule')
        super().__init__(*args, **kwargs)

        # Define o queryset para o campo 'plantas_destino'
        # Excluímos:
        # 1. A planta original do agendamento
        # 2. Plantas que já possuem um agendamento de rega
        self.fields['plantas_destino'].queryset = Plant.objects.filter(
            user=user
        ).exclude(
            pk=agendamento_a_clonar.planta.pk
        ).exclude(
            watering_schedule__isnull=False
        )        
        print(self.fields['plantas_destino'].queryset)