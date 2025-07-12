from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class WateringSchedule(models.Model):
    class FrequenciaChoices(models.TextChoices):
        DIARIA = 'DIARIA', 'Todos os dias'
        ALTERNADA = 'ALTERNADA', 'Dia sim, dia não'
        INTERVALO = 'INTERVALO', 'A cada X dias'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    planta = models.OneToOneField('plants.Plant', on_delete=models.CASCADE, related_name='watering_schedule', verbose_name="Planta")
    
    frequencia = models.CharField(max_length=20, choices=FrequenciaChoices.choices, verbose_name="Frequência")
    dias_intervalo = models.PositiveSmallIntegerField(
        null=True, blank=True, 
        verbose_name="Intervalo em dias",
        help_text="Preencha apenas se a frequência for 'A cada X dias'."
    )
    
    quantidade_agua_ml = models.PositiveIntegerField(verbose_name="Quantidade de Água (ml)")
    fertilizantes = models.ManyToManyField('fertilizer.Fertilizer', blank=True, verbose_name="Fertilizantes (opcional)")
    
    horario_preferencial = models.TimeField(default='08:00', verbose_name="Horário do Alerta")
    ultima_rega_registrada = models.DateField(
        null=True, blank=True, 
        verbose_name="Data da Última Rega", 
        help_text="Deixe em branco para começar hoje. Será atualizado automaticamente."
    )
    is_active = models.BooleanField(default=True, verbose_name="Agendamento Ativo")

    class Meta:
        verbose_name = "Agendamento de Rega"
        verbose_name_plural = "Agendamentos de Rega"
        ordering = ['planta__nome']

    def __str__(self):
        return f"Agendamento para {self.planta.nome}"

    @property
    def proxima_rega(self):
        """Calcula a data da próxima rega baseada na frequência e na última rega."""
        if not self.is_active:
            return None
            
        base_date = self.ultima_rega_registrada or timezone.now().date()
        
        if self.frequencia == self.FrequenciaChoices.DIARIA:
            return base_date + timedelta(days=1)
        elif self.frequencia == self.FrequenciaChoices.ALTERNADA:
            return base_date + timedelta(days=2)
        elif self.frequencia == self.FrequenciaChoices.INTERVALO and self.dias_intervalo:
            return base_date + timedelta(days=self.dias_intervalo)
        
        return base_date # Caso padrão ou inicial