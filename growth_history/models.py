from django.db import models
from django.conf import settings
from django.utils import timezone

class GrowthHistory(models.Model):
    planta = models.ForeignKey('plants.Plant', on_delete=models.CASCADE, related_name='historico')
    data_hora_evento = models.DateTimeField(default=timezone.now)
    tipo_evento = models.CharField(max_length=100, help_text="Ex: Mudança de Estágio, Poda, Foto, Observação")
    foto = models.ImageField(upload_to='growth_history/', blank=True, null=True)
    observacoes = models.TextField()

    class Meta:
        ordering = ['-data_hora_evento']

    def __str__(self):
        return f"Histórico de {self.planta.nome} - {self.tipo_evento}"