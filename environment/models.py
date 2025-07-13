from django.db import models
from django.conf import settings
from django.urls import reverse
from stage.models import Stage

class Environment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=200, blank=True)
    area = models.DecimalField(max_digits=5, decimal_places=2, help_text="Em m²")
    numero_maximo_plantas = models.PositiveIntegerField()
    estagio_preparado = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True, help_text="Selecione se o ambiente é otimizado para um estágio específico.")

    def __str__(self):
        return self.nome
        
    def get_absolute_url(self):
        return reverse('environment:update', kwargs={'pk': self.pk})

    @property
    def current_plant_count(self):
        # Acessa a contagem através do related_name 'plants' que o Django cria
        return self.plants.count()
        
    @property
    def is_full(self):
        return self.current_plant_count >= self.numero_maximo_plantas        