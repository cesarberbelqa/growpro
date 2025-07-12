from django.db import models
from django.conf import settings
from django.utils import timezone

class GrowthHistory(models.Model):
    # TORNAMOS O CAMPO 'user' NULO TEMPORARIAMENTE
    # Adicionamos null=True para permitir que a migração seja executada
    # em um banco de dados com linhas existentes.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='growth_histories',
        null=True, # <-- A MUDANÇA PRINCIPAL
        blank=True # Opcional, mas bom para formulários do admin
    )
    planta = models.ForeignKey('plants.Plant', on_delete=models.CASCADE, related_name='historico')
    
    data_hora_evento = models.DateTimeField(default=timezone.now)
    tipo_evento = models.CharField(max_length=100, help_text="Ex: Mudança de Estágio, Poda, Foto, Observação")
    foto = models.ImageField(upload_to='growth_history/', blank=True, null=True)
    observacoes = models.TextField()

    class Meta:
        verbose_name = "Histórico de Crescimento"
        verbose_name_plural = "Históricos de Crescimento"
        ordering = ['-data_hora_evento']

    def __str__(self):
        return f"Histórico de {self.planta.nome} em {self.data_hora_evento.strftime('%d/%m/%Y')}"