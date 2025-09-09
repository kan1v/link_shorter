from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages

from linktree import settings

from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        messages.success(self.request, "✅ Ви успішно увійшли в систему ")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "❌ Виникла помилка при вході в аккаунт. Перевірте введені дані.")
        return super().form_invalid(form)

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        messages.success(self.request, "✅ Ви успішно зареструвались ")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "❌ Виникла помилка при реєстрації аккаунту. Перевірте введені дані.")
        return super().form_invalid(form)

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'accounts/profile.html'

    def get_success_url(self):
        return reverse_lazy('accounts:profile')
    
    def get_object(self, queryset =None):
        return self.request.user 
    
    def form_valid(self, form):
        messages.success(self.request, "✅ Профіль успішно оновлено!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "❌ Виникла помилка при оновленні профілю. Перевірте введені дані.")
        return super().form_invalid(form)
        
class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'accounts/password_change_form.html'

    def form_valid(self, form):
        messages.success(self.request, "🔒 Пароль успішно змінено!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "❌ Помилка при зміні пароля. Спробуйте ще раз.")
        return super().form_invalid(form)


def logout_user(request):
    try:
        logout(request)
        messages.success(request, "Ви вийшли з аккаунту")
        return HttpResponseRedirect(reverse('accounts:login'))
    except Exception:
        messages.error(request, '❌ Помилка при виходу за аккаунту')

