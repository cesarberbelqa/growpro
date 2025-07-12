from django.db import models
from django.conf import settings
from django.urls import reverse

class Stage(models.Model):
    tipo_estagio = models.CharField(max_length=100, unique=True, help_text="Ex: Germinação, Vegetativo, Floração")
    duracao_em_dias = models.PositiveIntegerField()
    luz_diaria_em_horas = models.PositiveSmallIntegerField()
    ppfd = models.PositiveIntegerField(help_text="Photosynthetic Photon Flux Density")
    umidade_recomendada = models.CharField(max_length=20, help_text="Ex: 50%-60%")
    temperatura_recomendada = models.CharField(max_length=20, help_text="Ex: 20°C-25°C")

    def __str__(self):
        return self.tipo_estagio