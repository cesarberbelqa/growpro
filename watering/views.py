from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from .models import WateringSchedule
from .forms import WateringScheduleForm
from plants.models import Plant
from growth_history.models import GrowthHistory
from django.utils import timezone
from django.contrib import messages
from core.mixins import UserHasPlantsRequiredMixin
from django.views.generic.edit import FormView
from .forms import CloneWateringScheduleForm

class WateringScheduleListView(LoginRequiredMixin, UserHasPlantsRequiredMixin, ListView):
    model = WateringSchedule
    template_name = 'watering/schedule_list.html'
    context_object_name = 'schedules'

    def get_queryset(self):
        return WateringSchedule.objects.filter(user=self.request.user).select_related('planta')

class WateringScheduleCreateView(LoginRequiredMixin, UserHasPlantsRequiredMixin, CreateView):
    model = WateringSchedule
    form_class = WateringScheduleForm
    template_name = 'watering/schedule_form.html'
    success_url = reverse_lazy('watering:list')

    def get_initial(self):
        # Pré-seleciona a planta se o ID for passado na URL
        initial = super().get_initial()
        plant_id = self.request.GET.get('plant')
        if plant_id:
            initial['planta'] = get_object_or_404(Plant, pk=plant_id, user=self.request.user)
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class WateringScheduleUpdateView(LoginRequiredMixin, UserHasPlantsRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WateringSchedule
    form_class = WateringScheduleForm
    template_name = 'watering/schedule_form.html'
    success_url = reverse_lazy('watering:list')

    def test_func(self):
        schedule = self.get_object()
        return self.request.user == schedule.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class WateringScheduleDeleteView(LoginRequiredMixin, UserHasPlantsRequiredMixin, UserPassesTestMixin, DeleteView):
    model = WateringSchedule
    template_name = 'watering/schedule_confirm_delete.html'
    success_url = reverse_lazy('watering:list')

    def test_func(self):
        schedule = self.get_object()
        return self.request.user == schedule.user

# ==========================================================
#                   NOVA VIEW PARA REGAR AGORA
# ==========================================================
class WaterPlantNowView(LoginRequiredMixin, UserHasPlantsRequiredMixin, View):
    """
    View para registrar uma rega imediata para uma planta.
    Cria um registro no GrowthHistory.
    """
    def post(self, request, *args, **kwargs):
        # Usamos POST para garantir que ações que modificam dados não sejam feitas com um simples GET.
        planta = get_object_or_404(Plant, pk=self.kwargs['plant_pk'], user=request.user)
        
        # Opcional: Pegar a quantidade de água do agendamento, se houver.
        quantidade_agua = "não especificada"
        if hasattr(planta, 'watering_schedule') and planta.watering_schedule:
            quantidade_agua = f"{planta.watering_schedule.quantidade_agua_ml} ml"
            # Atualiza a data da última rega no agendamento
            planta.watering_schedule.ultima_rega_registrada = timezone.now().date()
            planta.watering_schedule.save()

        # Cria o registro no histórico de crescimento
        GrowthHistory.objects.create(
            user=request.user,
            planta=planta,
            tipo_evento="Rega Manual",
            observacoes=f"Planta regada. Quantidade: {quantidade_agua}."
        )

        messages.success(request, f"Rega registrada para a planta '{planta.nome}' com sucesso!")
        return redirect('plants:detail', pk=planta.pk)        

# ==========================================================
#               NOVA VIEW PARA CLONAGEM
# ==========================================================
class CloneWateringScheduleView(LoginRequiredMixin, FormView):
    template_name = 'watering/clone_schedule_form.html'
    form_class = CloneWateringScheduleForm

    def setup(self, request, *args, **kwargs):
        """ Pega o agendamento de origem da URL antes de tudo. """
        super().setup(request, *args, **kwargs)
        self.source_schedule = get_object_or_404(
            WateringSchedule,
            pk=self.kwargs['pk'],
            user=request.user
        )

    def get_form_kwargs(self):
        """ Passa argumentos extras para o __init__ do formulário. """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['source_schedule'] = self.source_schedule
        return kwargs

    def get_context_data(self, **kwargs):
        """ Adiciona o agendamento de origem ao contexto do template. """
        context = super().get_context_data(**kwargs)
        context['source_schedule'] = self.source_schedule
        form = context['form']
        context['has_target_plants'] = form.fields['plantas_destino'].queryset.exists()
        return context

    def form_valid(self, form):
        """ Executa a lógica de clonagem quando o formulário é válido. """
        plantas_selecionadas = form.cleaned_data['plantas_destino']
        
        fertilizantes_originais = list(self.source_schedule.fertilizantes.all())
        
        novos_agendamentos = []
        for planta in plantas_selecionadas:
            novo_agendamento = WateringSchedule(
                user=self.request.user,
                planta=planta,
                frequencia=self.source_schedule.frequencia,
                dias_intervalo=self.source_schedule.dias_intervalo,
                quantidade_agua_ml=self.source_schedule.quantidade_agua_ml,
                horario_preferencial=self.source_schedule.horario_preferencial,
                is_active=self.source_schedule.is_active,
                # A última rega não é clonada para que o ciclo comece agora.
            )
            novos_agendamentos.append(novo_agendamento)
            
        # Usa bulk_create para eficiência ao criar múltiplos objetos
        WateringSchedule.objects.bulk_create(novos_agendamentos)

        # Lida com a relação ManyToMany de fertilizantes após a criação
        for agendamento in novos_agendamentos:
            if fertilizantes_originais:
                agendamento.fertilizantes.set(fertilizantes_originais)

        messages.success(self.request, f"Agendamento clonado para {len(plantas_selecionadas)} planta(s) com sucesso!")
        return redirect('watering:list')        