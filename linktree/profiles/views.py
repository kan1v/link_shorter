from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import PublicProfileForm, SocialLinkFormSet, CustomButtonFormSet, UserForm
from .models import PublicProfile, ProfileClick
from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()

@login_required
def edit_public_profile(request):
    profile, _ = PublicProfile.objects.get_or_create(user=request.user)
    
    tab = request.GET.get("tab", "edit")  # выбираем вкладку
    profile = PublicProfile.objects.get(user=request.user)

    is_pro = profile.plan == "pro"
    is_premium = profile.plan == "premium"

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = PublicProfileForm(request.POST, request.FILES, instance=profile)
        social_formset = SocialLinkFormSet(request.POST, prefix='social', instance=profile)
        button_formset = CustomButtonFormSet(request.POST, prefix='button', instance=profile)

        if all([user_form.is_valid(), profile_form.is_valid(), social_formset.is_valid(), button_formset.is_valid()]):
            user_form.save()
            profile_form.save()
            social_formset.save()
            button_formset.save()
            messages.success(request, "Профіль оновлено успішно")
            return redirect(f"{request.path}?tab=edit")
        else:
            messages.error(request, "Помилка при збереженні профілю")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = PublicProfileForm(instance=profile)
        social_formset = SocialLinkFormSet(prefix='social', instance=profile)
        button_formset = CustomButtonFormSet(prefix='button', instance=profile)

    # Данные для аналитики
    clicks = profile.clicks.all()
    total_clicks = clicks.count()
    link_clicks = clicks.values('link').annotate(count=Count('id')).order_by('-count')

    return render(request, "profiles/edit_profile.html", {
        "tab": tab,
        "user_form": user_form,
        "profile_form": profile_form,
        "social_formset": social_formset,
        "button_formset": button_formset,
        "total_clicks": total_clicks,
        "link_clicks": link_clicks,
        "profile": profile,
        "is_pro": is_pro,
        "is_premium": is_premium,
    })


def public_profile_view(request, username):
    profile = get_object_or_404(PublicProfile, slug=username)
    return render(request, "profiles/public_profile.html", {"profile": profile})
