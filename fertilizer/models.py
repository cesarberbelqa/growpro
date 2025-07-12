from django.db import models
from django.conf import settings

class Fertilizer(models.Model):
    class Tipo(models.TextChoices):
        LIQUIDO = 'LIQUIDO', 'Líquido'
        SOLIDO = 'SOLIDO', 'Sólido'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    # quantidade_aplicada não faz sentido aqui, mas sim na rega.

    def __str__(self):
        return self.nome