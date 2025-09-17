from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import PublicProfileForm, SocialLinkFormSet, CustomButtonFormSet
from .models import PublicProfile

@login_required
def edit_public_profile(request):
    profile, created = PublicProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = PublicProfileForm(request.POST, instance=profile)
        social_formset = SocialLinkFormSet(request.POST, instance=profile, prefix="social")
        button_formset = CustomButtonFormSet(request.POST, instance=profile, prefix="button")

        if form.is_valid() and social_formset.is_valid() and button_formset.is_valid():
            with transaction.atomic():
                form.save()
                social_formset.save()
                button_formset.save()
                profile.generate_qr()
            messages.success(request, "Профіль оновлено!")
            return redirect('profiles:edit_public_profile')
    else:
        form = PublicProfileForm(instance=profile)
        social_formset = SocialLinkFormSet(instance=profile, prefix="social")
        button_formset = CustomButtonFormSet(instance=profile, prefix="button")

    return render(request, 'profiles/edit_profile.html', {
        'form': form,
        'social_formset': social_formset,
        'button_formset': button_formset
    })


def public_profile_view(request, username):
    profile = get_object_or_404(PublicProfile, slug=username)
    return render(request, "profiles/public_profile.html", {"profile": profile})
