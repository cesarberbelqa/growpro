from rest_framework import serializers
from .models import Plant

class PlantSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    estagio_atual_nome = serializers.ReadOnlyField(source='estagio_atual.tipo_estagio')
    precisa_mudar_estagio = serializers.ReadOnlyField()

    class Meta:
        model = Plant
        fields = [
            'id', 'nome', 'especie', 'strain', 'identificacao', 'ambiente_atual', 
            'estagio_atual', 'estagio_atual_nome', 'data_plantio', 'status', 'user', 
            'precisa_mudar_estagio'
        ]