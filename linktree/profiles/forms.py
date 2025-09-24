from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from .models import PublicProfile, SocialLink, CustomButton

User = get_user_model()



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
        }

class PublicProfileForm(forms.ModelForm):
    class Meta:
        model = PublicProfile
        fields = ["slug", "background_color", "background", "button_style"]
        widgets = {
            "slug": forms.TextInput(attrs={"class": "w-full px-4 py-2 border rounded-lg", "placeholder": "yourname"}),
            "background_color": forms.TextInput(attrs={"type": "color", "class": "w-16 h-10"}),
            "background": forms.ClearableFileInput(attrs={"class": "w-full py-2"}),
            "button_style": forms.Select(attrs={"class": "w-full px-4 py-2 border rounded-lg"}),
        }



class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ["name", "url"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "Instagram / Telegram / etc."
            }),
            "url": forms.URLInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "https://..."
            })
        }


class CustomButtonForm(forms.ModelForm):
    class Meta:
        model = CustomButton
        fields = ["title", "url", "order"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "Назва кнопки"
            }),
            "url": forms.URLInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "https://..."
            }),
            "order": forms.NumberInput(attrs={
                "class": "w-16 px-2 py-1 border rounded-lg",
                "min": 0
            }),
        }


# Inline formsets для соцсетей и кастомных кнопок
SocialLinkFormSet = inlineformset_factory(
    PublicProfile, SocialLink, form=SocialLinkForm,
    extra=1, can_delete=True
)

CustomButtonFormSet = inlineformset_factory(
    PublicProfile, CustomButton, form=CustomButtonForm,
    extra=1, can_delete=True
)
