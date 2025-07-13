from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404

from .models import GrowthHistory
from .forms import GrowthHistoryForm
from plants.models import Plant

class GrowthHistoryCreateView(LoginRequiredMixin, CreateView):
    model = GrowthHistory
    form_class = GrowthHistoryForm
    template_name = 'growth_history/history_form.html'

    def dispatch(self, request, *args, **kwargs):
        """ Pega a planta da URL e a armazena na instância da view. """
        self.planta = get_object_or_404(Plant, pk=self.kwargs['plant_pk'], user=self.request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """ Adiciona a planta ao contexto para o template. """
        context = super().get_context_data(**kwargs)
        context['planta'] = self.planta
        return context

    def form_valid(self, form):
        """ Associa o novo registro à planta e ao usuário antes de salvar. """
        form.instance.planta = self.planta
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """ Redireciona de volta para a página de detalhes da planta. """
        return reverse('plants:detail', kwargs={'pk': self.planta.pk})

class GrowthHistoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = GrowthHistory
    template_name = 'growth_history/history_confirm_delete.html'
    context_object_name = 'history_entry'

    def test_func(self):
        """ Garante que o usuário só possa deletar seus próprios registros. """
        entry = self.get_object()
        return self.request.user == entry.user

    def get_success_url(self):
        """ Redireciona de volta para a página de detalhes da planta. """
        planta_pk = self.object.planta.pk
        return reverse('plants:detail', kwargs={'pk': planta_pk})

class GrowthHistoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = GrowthHistory
    form_class = GrowthHistoryForm
    template_name = 'growth_history/history_form.html' # Reutilizaremos o mesmo formulário
    context_object_name = 'history_entry'

    def test_func(self):
        """ Garante que o usuário só possa editar seus próprios registros. """
        entry = self.get_object()
        return self.request.user == entry.user

    def get_context_data(self, **kwargs):
        """ Adiciona a planta ao contexto para o template. """
        context = super().get_context_data(**kwargs)
        # O objeto do histórico (self.object) já tem a planta, então podemos acessá-la
        context['planta'] = self.object.planta
        return context

    def get_success_url(self):
        """ Redireciona de volta para a página de detalhes da planta. """
        return reverse('plants:detail', kwargs={'pk': self.object.planta.pk})        