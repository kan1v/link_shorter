from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('edit/', views.edit_public_profile, name='edit_public_profile'),
    path('<str:username>/', views.public_profile_view, name='public_profile'),
]
