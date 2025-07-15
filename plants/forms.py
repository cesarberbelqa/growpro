from django import forms
from .models import Plant
from environment.models import Environment
from stage.models import Stage
from django.utils import timezone # <-- Adicione este import

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['nome', 'especie', 'strain', 'identificacao', 'ambiente_atual', 'estagio_atual', 'data_plantio', 'observacoes']
        widgets = {
            'data_plantio': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        # Filtra os dropdowns para mostrar apenas os itens do usuário logado
        self.fields['ambiente_atual'].queryset = Environment.objects.filter(user=user)
        self.fields['estagio_atual'].queryset = Stage.objects.all()

        # ==========================================================
        #           LÓGICA PARA PREENCHER A DATA
        # ==========================================================
        # Se o formulário é para criar uma nova planta (não tem instância salva ainda)
        if not self.instance.pk:
            # Define o valor inicial do campo 'data_plantio' para a data de hoje.
            self.fields['data_plantio'].initial = timezone.now().date()

    def clean_ambiente_atual(self):
        """
        Validação específica para o campo 'ambiente_atual'.
        """
        ambiente = self.cleaned_data.get('ambiente_atual')

        if not ambiente:
            return ambiente # Se nenhum ambiente for selecionado, não há o que validar.

        # Conta o número de plantas já existentes no ambiente
        plant_count = Plant.objects.filter(ambiente_atual=ambiente).count()


        # Lógica para edição: se estivermos editando uma planta que já está neste ambiente,
        # a contagem não deve incluí-la, pois não estamos adicionando uma nova planta.
        if self.instance and self.instance.pk and self.instance.ambiente_atual == ambiente:
             # Nenhuma validação necessária, pois a planta já ocupa um espaço.
             pass
        else:
            # Lógica para criação ou mudança de ambiente
            if plant_count >= ambiente.numero_maximo_plantas:
                raise forms.ValidationError(
                    f"O ambiente '{ambiente.nome}' já atingiu sua capacidade máxima de "
                    f"{ambiente.numero_maximo_plantas} planta(s)."
                )
        
        return ambiente