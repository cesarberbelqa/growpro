from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from .models import Plant
from .forms import PlantForm
from rest_framework import viewsets
from .serializers import PlantSerializer
from environment.models import Environment # <-- Adicione este import
from stage.models import Stage      
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from collections import defaultdict
from environment.models import Environment
from core.mixins import StageExistsRequiredMixin
from growth_history.models import GrowthHistory
from django.utils import timezone

# --- Views para o Frontend ---

class PlantListView(LoginRequiredMixin, ListView):
    # Não vamos mais usar o 'model' e 'queryset' padrão da ListView,
    # pois vamos construir nosso próprio contexto.
    template_name = 'plants/plant_list.html'
    context_object_name = 'grouped_plants' # Novo nome para o contexto

    def get_queryset(self):
        """
        Sobrescrevemos o queryset para agrupar as plantas por ambiente.
        """
        # Filtra todas as plantas do usuário
        plants = Plant.objects.filter(user=self.request.user).select_related(
            'ambiente_atual', 'estagio_atual'
        ).order_by('data_plantio', 'nome') # <-- Ordena por data de plantio e nome
        
        # Cria um dicionário para agrupar as plantas
        grouped = defaultdict(list)
        
        # Plantas sem ambiente definido
        unassigned_plants = []
        
        for plant in plants:
            if plant.ambiente_atual:
                grouped[plant.ambiente_atual].append(plant)
            else:
                unassigned_plants.append(plant)
        
        # Converte o defaultdict para um dict normal para o template
        # e o ordena pelo nome do ambiente
        sorted_grouped = dict(sorted(grouped.items(), key=lambda item: item[0].id))

        # Adiciona as plantas sem ambiente em uma chave especial
        if unassigned_plants:
            sorted_grouped['Sem Ambiente'] = unassigned_plants
        
        return sorted_grouped
    
    # Vamos adicionar o get_context_data de volta para a verificação no template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_environments'] = Environment.objects.filter(user=self.request.user).exists()
        context['has_stages_in_system'] = Stage.objects.exists()
        return context

class PlantDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Plant
    template_name = 'plants/plant_detail.html'

    def test_func(self):
        plant = self.get_object()
        return self.request.user == plant.user

class PlantCreateView(LoginRequiredMixin, StageExistsRequiredMixin, CreateView):
    model = Plant
    form_class = PlantForm
    template_name = 'plants/plant_form.html'
    success_url = reverse_lazy('plants:list')

    # Remova o método dispatch() que adicionamos antes.
    # def dispatch(self, request, *args, **kwargs):
    #    ...

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PlantUpdateView(LoginRequiredMixin, StageExistsRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Plant
    form_class = PlantForm
    template_name = 'plants/plant_form.html'

    def test_func(self):
        plant = self.get_object()
        return self.request.user == plant.user
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        """
        Redireciona para a URL passada no campo 'next', ou para a lista de plantas
        como um fallback de segurança.
        """
        # Procura por um parâmetro 'next' no POST do formulário
        next_url = self.request.POST.get('next', None)
        if next_url:
            # Uma verificação de segurança básica para evitar redirecionamento para outros sites
            # (Open Redirect Attack). Isso garante que a URL é relativa ao nosso site.
            # if next_url.startswith('/'):
            return next_url 
        
        # Se 'next' não for fornecido ou for inválido, retorna para a lista de plantas.
        return reverse_lazy('plants:list')

    def get_context_data(self, **kwargs):
        """
        Adiciona a URL da página atual ao contexto para ser usada no formulário.
        """
        context = super().get_context_data(**kwargs)
        # request.META.get('HTTP_REFERER') pega a URL da página anterior.
        # Usamos request.get_full_path() como fallback se o referer não estiver disponível.
        context['next'] = self.request.META.get('HTTP_REFERER', self.request.get_full_path())
        return context

class PlantDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Plant
    template_name = 'plants/plant_confirm_delete.html'
    success_url = reverse_lazy('plants:list')

    def test_func(self):
        plant = self.get_object()
        return self.request.user == plant.user

# --- ViewSet para a API ---

class PlantViewSet(viewsets.ModelViewSet):
    serializer_class = PlantSerializer
    
    def get_queryset(self):
        # Garante que a API só retorne plantas do usuário autenticado
        return Plant.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associa o usuário autenticado ao criar um novo objeto
        serializer.save(user=self.request.user)

class TransitionStageView(LoginRequiredMixin, View):
    """ View para processar a transição de estágio de uma planta. """
    def get(self, request, *args, **kwargs):
        planta = get_object_or_404(Plant, pk=self.kwargs['pk'], user=request.user)
        
        proximo_estagio = planta.proximo_estagio_disponivel
        
        if not proximo_estagio:
            messages.error(request, 'Não há um próximo estágio definido para o estágio atual desta planta.')
            return redirect('plants:list')
            
        if not planta.precisa_mudar_estagio:
            messages.warning(request, 'Esta planta ainda não atingiu o tempo necessário para mudar de estágio.')
            return redirect('plants:list')

        # Armazena o estágio antigo para o registro de histórico
        estagio_antigo = planta.estagio_atual.tipo_estagio

        # Executa a transição
        planta.estagio_atual = proximo_estagio
        planta.data_ultima_mudanca_estagio = timezone.now().date()
        planta.save()
        
        # Cria um registro no histórico
        GrowthHistory.objects.create(
            user=request.user,
            planta=planta,
            tipo_evento="Mudança de Estágio",
            observacoes=f"A planta foi movida do estágio '{estagio_antigo}' para '{proximo_estagio.tipo_estagio}'."
        )

        messages.success(request, f"A planta '{planta.nome}' foi movida para o estágio '{proximo_estagio.tipo_estagio}' com sucesso!")
        return redirect('plants:list')        