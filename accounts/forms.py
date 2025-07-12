from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from datetime import date, timedelta

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'consentimento_marketing', 'first_name', 'last_name', 'data_nascimento', 'pais')
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if data_nascimento:
            limite_idade = date.today() - timedelta(days=18 * 365.25)
            if data_nascimento > limite_idade:
                raise forms.ValidationError("Você deve ter pelo menos 18 anos para se cadastrar.")
        return data_nascimento

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'consentimento_marketing', 'first_name', 'last_name', 'data_nascimento', 'pais', 'is_active', 'is_staff')
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

class UserProfileForm(forms.ModelForm):
    """
    Formulário para que o próprio usuário edite suas informações de perfil.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'data_nascimento', 'pais']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_data_nascimento(self):
        # Reutilizamos a validação de idade para consistência
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if data_nascimento:
            limite_idade = date.today() - timedelta(days=18 * 365.25)
            if data_nascimento > limite_idade:
                raise forms.ValidationError("Você deve ter pelo menos 18 anos.")
        return data_nascimento