from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin

from environment.models import Environment
from stage.models import Stage

class PlantPrerequisitesMixin(AccessMixin):
    """
    Mixin que verifica se o usuário tem os pré-requisitos (Ambientes e Estágios)
    para acessar as views relacionadas a plantas.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        user = request.user
        has_environments = Environment.objects.filter(user=user).exists()
        has_stages = Stage.objects.exists()

        if not has_environments:
            messages.info(request, 'Você precisa cadastrar pelo menos um Ambiente antes de gerenciar suas plantas.')
            return redirect('environment:list')

        if not has_stages:
            messages.warning(request, 'Nenhum Estágio de cultivo foi cadastrado no sistema. Por favor, contate o administrador.')
            return redirect('plants:list')

        return super().dispatch(request, *args, **kwargs)