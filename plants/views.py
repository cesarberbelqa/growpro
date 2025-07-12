from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Plant
from .forms import PlantForm
from rest_framework import viewsets
from .serializers import PlantSerializer
from environment.models import Environment # <-- Adicione este import
from stage.models import Stage      
from django.shortcuts import redirect
from django.contrib import messages
from .mixins import PlantPrerequisitesMixin

# --- Views para o Frontend ---

class PlantListView(LoginRequiredMixin, PlantPrerequisitesMixin, ListView):
    model = Plant
    template_name = 'plants/plant_list.html'
    context_object_name = 'plants'

    def get_queryset(self):
        return Plant.objects.filter(user=self.request.user).select_related('estagio_atual', 'ambiente_atual')

class PlantDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Plant
    template_name = 'plants/plant_detail.html'

    def test_func(self):
        plant = self.get_object()
        return self.request.user == plant.user

class PlantCreateView(LoginRequiredMixin, PlantPrerequisitesMixin, CreateView):
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

class PlantUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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