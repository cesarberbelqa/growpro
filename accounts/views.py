from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, UserProfileForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

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