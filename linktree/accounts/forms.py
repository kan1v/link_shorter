import datetime
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none",
                "placeholder": "Введіть email або username",
            }
        ),
        label="Email або username"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none",
                "placeholder": "Введіть пароль",
            }
        ),
        label="Пароль"
    )



    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
        labels = {
            'username': 'Username',
            'password': 'Пароль',
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none",
                "placeholder": "Введіть username",
            }
        )
    )
    password1 = forms.CharField(label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none",
                "placeholder": "Введіть пароль",
            }
        )
    )
    password2 = forms.CharField(label='Підтвердіть пароль',
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none",
                "placeholder": "Підтвердіть пароль",
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'username': 'Username',
            'email': 'E-mail',
            'first_name': 'Ім’я',
            'last_name': 'Прізвище',
            'password1': 'Пароль',
            'password2': 'Підтвердження пароля',
        }
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    "class": "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none",
                    "placeholder": "Введіть e-mail",
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none",
                    "placeholder": "Введіть ім’я",
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none",
                    "placeholder": "Введіть прізвище",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такий email вже зайнятий")
        return email
    
class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(
        label='Логін',
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none",
                "placeholder": "Введіть логін",
            }
        )
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none",
                "placeholder": "Введіть email",
            }
        )
    )
    first_name = forms.CharField(
        label='Імʼя',
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none",
                "placeholder": "Введіть імʼя",
            }
        )
    )
    last_name = forms.CharField(
        label='Прізвище',
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none",
                "placeholder": "Введіть прізвище",
            }
        )
    )
    bio = forms.CharField(
        label='Опис',
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none",
                "placeholder": "Короткий опис про себе",
                "rows": 4
            }
        )
    )
    avatar = forms.ImageField(
        label='Фото профілю',
        required=False,
    )

    class Meta:
        model = get_user_model()
        fields = ['avatar', 'username', 'email', 'bio', 'first_name', 'last_name']


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Старий пароль',
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none",
                "placeholder": "Введіть старий пароль",
            }
        )
    )
    new_password1 = forms.CharField(
        label='Новий пароль',
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none",
                "placeholder": "Введіть новий пароль",
            }
        )
    )
    new_password2 = forms.CharField(
        label='Підтвердження пароля',
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none",
                "placeholder": "Повторіть новий пароль",
            }
        )
    )