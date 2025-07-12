from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from plants.models import Plant
from collections import defaultdict

class Command(BaseCommand):
    help = 'Verifica se alguma planta precisa mudar de estágio e notifica o usuário por e-mail.'

    def handle(self, *args, **options):
        plantas_a_notificar = Plant.objects.filter(status='Ativa')
        
        # Agrupa as plantas por usuário
        user_notifications = defaultdict(list)
        
        for planta in plantas_a_notificar:
            if planta.precisa_mudar_estagio:
                user_notifications[planta.user].append(planta)
        
        if not user_notifications:
            self.stdout.write(self.style.SUCCESS('Nenhuma planta precisa de mudança de estágio hoje.'))
            return
            
        for user, plants in user_notifications.items():
            self.stdout.write(self.style.WARNING(f"Notificando {user.email}..."))
            
            subject = "GrowPro - Alerta de Mudança de Estágio"
            plant_list_str = "\n".join([f"- {p.nome} ({p.identificacao})" for p in plants])
            
            message = (
                f"Olá {user.first_name},\n\n"
                f"As seguintes plantas precisam de atenção para mudança de estágio:\n"
                f"{plant_list_str}\n\n"
                "Acesse o sistema para mais detalhes.\n\n"
                "Atenciosamente,\nEquipe GrowPro"
            )
            
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                self.stdout.write(self.style.SUCCESS(f"  > E-mail enviado para {user.email} com {len(plants)} planta(s)."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  > Falha ao enviar e-mail para {user.email}: {e}"))