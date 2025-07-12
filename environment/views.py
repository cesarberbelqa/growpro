from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Environment
from .forms import EnvironmentForm
from stage.models import Stage

class EnvironmentListView(LoginRequiredMixin, ListView):
    model = Environment
    template_name = 'environments/environment_list.html'
    context_object_name = 'environments'

    def get_queryset(self):
        return Environment.objects.filter(user=self.request.user).select_related('estagio_preparado')

    def get_context_data(self, **kwargs):
        """ Adiciona dados extras ao contexto do template. """
        context = super().get_context_data(**kwargs)
        # Passa a informação booleana para o template
        context['has_stages'] = Stage.objects.exists()
        return context

class EnvironmentCreateView(LoginRequiredMixin, CreateView):
    model = Environment
    form_class = EnvironmentForm
    template_name = 'environments/environment_form.html'
    success_url = reverse_lazy('environment:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EnvironmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Environment
    form_class = EnvironmentForm
    template_name = 'environments/environment_form.html'
    success_url = reverse_lazy('environment:list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        environment = self.get_object()
        return self.request.user == environment.user

class EnvironmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Environment
    template_name = 'environments/environment_confirm_delete.html'
    success_url = reverse_lazy('environment:list')

    def test_func(self):
        environment = self.get_object()
        return self.request.user == environment.user