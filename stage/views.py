from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Stage
from .forms import StageForm

class StageListView(LoginRequiredMixin, ListView):
    model = Stage
    template_name = 'stages/stage_list.html'
    context_object_name = 'stages'

    def get_queryset(self):
        # Garante que o usuário só veja seus próprios estágios
        return Stage.objects.filter(user=self.request.user)

class StageCreateView(LoginRequiredMixin, CreateView):
    model = Stage
    form_class = StageForm
    template_name = 'stages/stage_form.html'
    success_url = reverse_lazy('stage:list')

    def form_valid(self, form):
        # Associa o estágio ao usuário logado antes de salvar
        form.instance.user = self.request.user
        return super().form_valid(form)

class StageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Stage
    form_class = StageForm
    template_name = 'stages/stage_form.html'
    success_url = reverse_lazy('stage:list')

    def test_func(self):
        # Garante que o usuário só edite seus próprios estágios
        stage = self.get_object()
        return self.request.user == stage.user

class StageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Stage
    template_name = 'stages/stage_confirm_delete.html'
    success_url = reverse_lazy('stage:list')

    def test_func(self):
        # Garante que o usuário só exclua seus próprios estágios
        stage = self.get_object()
        return self.request.user == stage.user