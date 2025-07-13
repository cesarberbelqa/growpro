from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin

from stage.models import Stage
from environment.models import Environment

class StageExistsRequiredMixin(AccessMixin):
    """
    Verifica se existe pelo menos um Stage CADASTRADO NO SISTEMA.
    Este é um pré-requisito global.
    """
    def dispatch(self, request, *args, **kwargs):
        if not Stage.objects.exists():
            messages.error(request, 'Não há estágios de cultivo configurados no sistema. Por favor, contate o administrador.')
            # Redireciona para uma página segura, como a home ou o dashboard.
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class EnvironmentExistsRequiredMixin(AccessMixin):
    """
    Verifica se o USUÁRIO LOGADO tem pelo menos um Environment.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not Environment.objects.filter(user=request.user).exists():
            messages.info(request, 'Você precisa cadastrar um Ambiente antes de adicionar uma planta.')
            return redirect('environment:list')
        
        return super().dispatch(request, *args, **kwargs)