from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail
from django.utils import timezone
from django.conf import settings
from collections import defaultdict
from watering.models import WateringSchedule

class Command(BaseCommand):
    help = 'Verifica agendamentos e envia alertas de rega por e-mail.'

    def handle(self, *args, **options):
        hoje = timezone.now().date()
        self.stdout.write(f"Iniciando verificação de regas para o dia {hoje.strftime('%d/%m/%Y')}...")

        # Filtra apenas agendamentos ativos
        schedules = WateringSchedule.objects.filter(is_active=True).select_related('user', 'planta')
        
        # Agrupa as notificações por usuário
        user_notifications = defaultdict(list)
        
        for schedule in schedules:
            if schedule.proxima_rega == hoje:
                user_notifications[schedule.user].append(schedule)
        
        if not user_notifications:
            self.stdout.write(self.style.SUCCESS('Nenhum alerta de rega para hoje.'))
            return

        datatuple = []
        for user, user_schedules in user_notifications.items():
            self.stdout.write(f"Preparando e-mail para {user.email}...")
            
            subject = "GrowPro - Lembrete de Rega de Hoje"
            
            schedule_list_str = "\n".join(
                [f"- {s.planta.nome}: {s.quantidade_agua_ml}ml" for s in user_schedules]
            )
            
            message = (
                f"Olá {user.first_name},\n\n"
                f"Lembrete para regar as seguintes plantas hoje:\n\n"
                f"{schedule_list_str}\n\n"
                "Após regar, lembre-se de registrar a ação no sistema para manter o histórico atualizado.\n\n"
                "Atenciosamente,\nEquipe GrowPro"
            )
            
            datatuple.append((subject, message, settings.DEFAULT_FROM_EMAIL, [user.email]))
        
        try:
            send_mass_mail(datatuple, fail_silently=False)
            self.stdout.write(self.style.SUCCESS(f"Total de {len(datatuple)} e-mails de alerta enviados com sucesso!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ocorreu um erro ao enviar os e-mails: {e}"))