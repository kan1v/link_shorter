from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("webhook/stripe/", views.stripe_webhook, name="stripe-webhook"),
    path("ckeckot/<str:plan>/", views.create_stripe_checkout_session, name="create_checkout"),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.payment_cancel, name='cancel'),

]