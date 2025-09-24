from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import PublicProfileForm, SocialLinkFormSet, CustomButtonFormSet, UserForm
from .models import PublicProfile
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def edit_public_profile(request):
    profile, _ = PublicProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # Создаём формы
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = PublicProfileForm(request.POST, request.FILES, instance=profile)
        social_formset = SocialLinkFormSet(request.POST, prefix='social', instance=profile)
        button_formset = CustomButtonFormSet(request.POST, prefix='button', instance=profile)

        if user_form.is_valid() and profile_form.is_valid() and social_formset.is_valid() and button_formset.is_valid():
            try:
                with transaction.atomic():
                    user_form.save()
                    profile_form.save()
                    social_formset.save()
                    button_formset.save()
                messages.success(request, "Профіль успішно збережено")
                return redirect("profiles:public_profile", username=request.user.username)
            except Exception as e:
                messages.error(request, f"Помилка збереження: {e}")
        else:
            messages.error(request, "Форма не валідна, перевірте всі поля")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = PublicProfileForm(instance=profile)
        social_formset = SocialLinkFormSet(prefix='social', instance=profile)
        button_formset = CustomButtonFormSet(prefix='button', instance=profile)

    return render(request, "profiles/edit_profile.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "social_formset": social_formset,
        "button_formset": button_formset,
    })



def public_profile_view(request, username):
    profile = get_object_or_404(PublicProfile, slug=username)
    return render(request, "profiles/public_profile.html", {"profile": profile})
