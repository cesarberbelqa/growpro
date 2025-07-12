from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

class Plant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='plants')
    nome = models.CharField(max_length=100)
    identificacao = models.CharField(max_length=50, help_text="Um ID único para a planta. Ex: SK-01")
    ambiente_atual = models.ForeignKey('environment.Environment', on_delete=models.SET_NULL, null=True, blank=True)
    estagio_atual = models.ForeignKey('stage.Stage', on_delete=models.PROTECT)
    data_plantio = models.DateField()
    observacoes = models.TextField(blank=True)
    status = models.CharField(max_length=50, default="Ativa")

    class Meta:
        unique_together = ('user', 'identificacao')

    def __str__(self):
        return f"{self.nome} ({self.identificacao})"

    def get_absolute_url(self):
        return reverse('plants:detail', kwargs={'pk': self.pk})

    @property
    def data_proxima_mudanca(self):
        if self.estagio_atual and self.estagio_atual.duracao_em_dias:
            return self.data_plantio + timedelta(days=self.estagio_atual.duracao_em_dias)
        return None

    @property
    def precisa_mudar_estagio(self):
        prox_mudanca = self.data_proxima_mudanca
        if prox_mudanca:
            return timezone.now().date() >= prox_mudanca
        return False