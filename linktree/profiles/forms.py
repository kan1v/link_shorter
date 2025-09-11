from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from .models import PublicProfile, SocialLink, CustomButton

User = get_user_model()


class PublicProfileForm(forms.ModelForm):
    username = forms.CharField(
        label="Логін",
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500",
            "placeholder": "Введіть логін",
        })
    )
    first_name = forms.CharField(
        label="Ім'я",
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-2 border rounded-lg",
            "placeholder": "Введіть ім'я",
        })
    )
    last_name = forms.CharField(
        label="Прізвище",
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-2 border rounded-lg",
            "placeholder": "Введіть прізвище",
        })
    )
    bio = forms.CharField(
        label="Опис",
        required=False,
        widget=forms.Textarea(attrs={
            "class": "w-full px-4 py-2 border rounded-lg",
            "rows": 4,
            "placeholder": "Короткий опис про себе",
        })
    )
    avatar = forms.ImageField(label="Фото профілю", required=False)

    class Meta:
        model = PublicProfile
        fields = ["username", "first_name", "last_name", "bio", "avatar", "slug", "background_color", "button_style"]
        widgets = {
            "slug": forms.TextInput(attrs={"class": "w-full px-4 py-2 border rounded-lg", "placeholder": "yourname"}),
            "background_color": forms.TextInput(attrs={"type": "color", "class": "w-16 h-10"}),
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
