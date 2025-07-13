from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, UserProfileForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    # A success_url não será mais usada diretamente, pois faremos o redirect manual
    # success_url = reverse_lazy('login') 
    template_name = 'registration/register.html'

    def form_valid(self, form):
        """
        Este método é chamado quando o formulário de criação é válido.
        Vamos sobrescrevê-lo para logar o usuário após o registro.
        """
        # Salva o novo usuário no banco de dados e o retorna
        user = form.save()
        
        # Loga o usuário recém-criado na sessão atual
        login(self.request, user)
        
        # Adiciona uma mensagem de boas-vindas (opcional)
        messages.success(self.request, f"Bem-vindo ao GrowPro, {user.first_name}! Seu registro foi concluído com sucesso.")
        
        # Redireciona para a página principal ou dashboard
        return redirect('home') # Ou 'plants:list', ou qualquer outra página que preferir

@login_required
def profile_view(request):
    if request.method == 'POST':
        # Processa o formulário enviado com os dados do usuário atual
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('profile')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        # Mostra o formulário preenchido com os dados atuais do usuário
        form = UserProfileForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'accounts/profile.html', context)