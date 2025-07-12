from django.db import models
from django.conf import settings

class EmailTemplate(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    assunto = models.CharField(max_length=200)
    corpo_html = models.TextField()
    corpo_texto = models.TextField(help_text="Versão em texto puro do e-mail.")

    def __str__(self):
        return self.nome

class Campaign(models.Model):
    class Status(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        ENVIANDO = 'ENVIANDO', 'Enviando'
        ENVIADA = 'ENVIADA', 'Enviada'

    template = models.ForeignKey(EmailTemplate, on_delete=models.PROTECT)
    enviada_em = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    # O registro dos destinatários será feito no histórico de envio para maior detalhe

    def __str__(self):
        return f"Campanha: {self.template.nome} - {self.status}"