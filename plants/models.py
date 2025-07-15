from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

class Plant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='plants')
    nome = models.CharField(max_length=100)
    especie = models.CharField(
        max_length=100,
        blank=True, # Torna o campo opcional no formulário
        help_text="Ex: Sativa, Indica, Híbrida, Tomate Cereja, etc."
    )
    strain = models.CharField(
        max_length=100,
        blank=True, # Também opcional
        verbose_name="Variedade/Strain",
        help_text="Ex: Skunk #1, Runtz, Coração de Boi, etc."
    )
    identificacao = models.CharField(max_length=50, help_text="Um ID único para a planta. Ex: SK-01")
    ambiente_atual = models.ForeignKey(
    'environment.Environment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='plants' # <-- ADICIONE/MODIFIQUE ISTO
    )
    estagio_atual = models.ForeignKey('stage.Stage', on_delete=models.PROTECT)
    data_plantio = models.DateField()
    observacoes = models.TextField(blank=True)
    status = models.CharField(max_length=50, default="Ativa")
    data_ultima_mudanca_estagio = models.DateField(
        null=True, blank=True, 
        help_text="Data da última transição de estágio. Preenchido automaticamente."
    )

    class Meta:
        unique_together = ('user', 'identificacao')

    def __str__(self):
        return f"{self.nome} ({self.identificacao})"

    def get_absolute_url(self):
        return reverse('plants:detail', kwargs={'pk': self.pk})

    @property
    def data_base_calculo_estagio(self):
        """ Retorna a data base para o cálculo da duração do estágio. """
        # Se houver data de última mudança, usa ela. Senão, usa a data de plantio.
        return self.data_ultima_mudanca_estagio or self.data_plantio

    @property
    def data_proxima_mudanca(self):
        """ Calcula a data da próxima mudança com base na nova data de referência. """
        if self.estagio_atual and self.estagio_atual.duracao_em_dias:
            return self.data_base_calculo_estagio + timedelta(days=self.estagio_atual.duracao_em_dias)
        return None

    @property
    def precisa_mudar_estagio(self):
        """ Verifica se o tempo do estágio atual expirou. """
        prox_mudanca = self.data_proxima_mudanca
        if prox_mudanca:
            return timezone.now().date() >= prox_mudanca
        return False
        
    @property
    def proximo_estagio_disponivel(self):
        """ Retorna o próximo estágio definido na tabela de transição, se houver. """
        if self.estagio_atual:
            return self.estagio_atual.proximo_estagio_definido
        return None

    # ==========================================================
    #           NOVA PROPRIEDADE PARA VERIFICAÇÃO
    # ==========================================================
    @property
    def is_stage_incompatible(self):
        """
        Retorna True se a planta está em um ambiente que tem um estágio
        preparado diferente do estágio atual da planta.
        """
        # A verificação só faz sentido se todos os três elementos existirem:
        # 1. A planta tem um ambiente.
        # 2. Esse ambiente tem um estágio preparado definido.
        # 3. A planta tem um estágio atual.
        if (self.ambiente_atual and 
            self.ambiente_atual.estagio_preparado and 
            self.estagio_atual):
            
            # Compara o estágio da planta com o estágio preparado do ambiente
            return self.ambiente_atual.estagio_preparado != self.estagio_atual
        
        # Se qualquer uma das condições acima for falsa, não há incompatibilidade.
        return False        