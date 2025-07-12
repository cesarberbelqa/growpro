from django import forms
from .models import Plant
from environment.models import Environment
from stage.models import Stage

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['nome', 'identificacao', 'ambiente_atual', 'estagio_atual', 'data_plantio', 'observacoes']
        widgets = {
            'data_plantio': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        # Filtra os dropdowns para mostrar apenas os itens do usuário logado
        self.fields['ambiente_atual'].queryset = Environment.objects.filter(user=user)
        self.fields['estagio_atual'].queryset = Stage.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        ambiente = cleaned_data.get('ambiente_atual')
        estagio = cleaned_data.get('estagio_atual')

        if ambiente and estagio:
            if ambiente.estagio_preparado and ambiente.estagio_preparado != estagio:
                self.add_error('ambiente_atual',
                    f"Atenção: O ambiente '{ambiente.nome}' é preparado para o estágio "
                    f"'{ambiente.estagio_preparado.tipo_estagio}', que é diferente do estágio da planta."
                )
        return cleaned_data