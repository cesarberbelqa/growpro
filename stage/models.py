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

    # Adicionar uma propriedade para facilitar o acesso à transição
    @property
    def proximo_estagio_definido(self):
        # Tenta encontrar uma transição que se origina deste estágio
        transicao = StageTransition.objects.filter(estagio_atual=self).first()
        if transicao:
            return transicao.proximo_estagio
        return None

# ==========================================================
#                   NOVO MODELO DE TRANSIÇÃO
# ==========================================================
class StageTransition(models.Model):
    """ Define a sequência de estágios. Ex: Germinação -> Vegetativo """
    estagio_atual = models.OneToOneField(
        Stage,
        on_delete=models.CASCADE,
        related_name='transicao_de',
        verbose_name="Do Estágio",
        unique=True, # Garante que cada estágio só pode ter uma transição de saída
    )
    proximo_estagio = models.ForeignKey(
        Stage,
        on_delete=models.CASCADE,
        related_name='transicao_para',
        verbose_name="Para o Estágio"
    )

    class Meta:
        verbose_name = "Transição de Estágio"
        verbose_name_plural = "Transições de Estágio"
        constraints = [
            models.UniqueConstraint(fields=['estagio_atual', 'proximo_estagio'], name='transicao_unica')
        ]

    def __str__(self):
        return f"{self.estagio_atual.tipo_estagio} → {self.proximo_estagio.tipo_estagio}"        