from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'age']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'data_nascimento', 'pais')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Marketing', {'fields': ('consentimento_marketing',)}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'data_nascimento', 'pais', 'password', 'password2'),
        }),
    )