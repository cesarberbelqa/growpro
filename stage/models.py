from django.db import models
from django.conf import settings
from django.urls import reverse

class Stage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo_estagio = models.CharField(max_length=100, help_text="Ex: Germinação, Vegetativo, Floração")
    duracao_em_dias = models.PositiveIntegerField()
    luz_diaria_em_horas = models.PositiveSmallIntegerField()
    ppfd = models.PositiveIntegerField(help_text="Photosynthetic Photon Flux Density")
    umidade_recomendada = models.CharField(max_length=20, help_text="Ex: 50%-60%")
    temperatura_recomendada = models.CharField(max_length=20, help_text="Ex: 20°C-25°C")

    def __str__(self):
        return f"{self.tipo_estagio} ({self.user.email})"
    
    def get_absolute_url(self):
        # Retorna a URL para a página de edição deste estágio específico
        return reverse('stage:update', kwargs={'pk': self.pk})