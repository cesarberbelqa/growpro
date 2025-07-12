from django import forms
from .models import Environment
from stage.models import Stage

class EnvironmentForm(forms.ModelForm):
    class Meta:
        model = Environment
        fields = ['nome', 'localizacao', 'area', 'numero_maximo_plantas', 'estagio_preparado']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtra o queryset para mostrar apenas os estágios do usuário logado
        self.fields['estagio_preparado'].queryset = Stage.objects.all()

        # Se não houver estágios, remove o campo do formulário
        if not stages_queryset.exists():
            del self.fields['estagio_preparado']