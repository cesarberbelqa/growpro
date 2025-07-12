from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from .models import WateringSchedule
from .forms import WateringScheduleForm
from plants.models import Plant

class WateringScheduleListView(LoginRequiredMixin, ListView):
    model = WateringSchedule
    template_name = 'watering/schedule_list.html'
    context_object_name = 'schedules'

    def get_queryset(self):
        return WateringSchedule.objects.filter(user=self.request.user).select_related('planta')

class WateringScheduleCreateView(LoginRequiredMixin, CreateView):
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

class WateringScheduleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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

class WateringScheduleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = WateringSchedule
    template_name = 'watering/schedule_confirm_delete.html'
    success_url = reverse_lazy('watering:list')

    def test_func(self):
        schedule = self.get_object()
        return self.request.user == schedule.user