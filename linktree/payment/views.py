# app_subscriptions/views.py

import logging
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
import stripe

from profiles.models import PublicProfile

logger = logging.getLogger(__name__)

# Устанавливаем API-ключ Stripe (секретный) — обязательно хранить в settings/env
stripe.api_key = settings.STRIPE_SECRET_KEY
# Секрет вебхука (тот, что в Dashboard → Webhooks)
STRIPE_WEBHOOK_SECRET = settings.STRIPE_WEBHOOK_SECRET


@require_POST
def create_stripe_checkout_session(request, plan):
    """
    Создаёт Stripe Checkout Session в режиме subscription для тарифов "pro" и "premium".
    Ожидается POST-запрос (например, форма или ajax), в котором:
      - request.user может быть аутентифицирован — тогда мы укажем client_reference_id,
      - либо можно передать поле 'email' в POST для анонимного пользователя.
    """
    price_lookup = {
        "pro": settings.STRIPE_PRICE_PRO,
        "premium": settings.STRIPE_PRICE_PREMIUM,
    }

    if plan not in price_lookup:
        return HttpResponseBadRequest("Неверный тариф")

    # Попробуем взять email из аутентифицированного пользователя или из POST
    customer_email = None
    client_reference_id = None
    if request.user.is_authenticated:
        if request.user.email:
            customer_email = request.user.email
        client_reference_id = str(request.user.id)
    else:
        # если аноним, можно передать email в форме (опционально)
        customer_email = request.POST.get("email")

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{
                "price": price_lookup[plan],
                "quantity": 1,
            }],
            success_url=request.build_absolute_uri(reverse("payment:success")) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse("payment:cancel")),
            # передаём user id чтобы потом по webhook привязать профиль надежно
            client_reference_id=client_reference_id,
            # если есть — указываем email, чтобы он подтянулся в session.customer_details
            customer_email=customer_email,
        )
        return redirect(checkout_session.url, code=303)
    except stripe.error.StripeError as e:
        logger.exception("Stripe error while creating checkout session")
        return HttpResponseBadRequest(f"Stripe error: {str(e)}")
    except Exception as e:
        logger.exception("Unexpected error while creating checkout session")
        return HttpResponseBadRequest(str(e))


@csrf_exempt
def stripe_webhook(request):
    """
    Обработка вебхуков от Stripe.
    Подписки/оплаты приходят сюда — обновляем PublicProfile.
    """
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    if sig_header is None:
        logger.warning("Missing Stripe signature header")
        return HttpResponse(status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Невалидный payload
        logger.exception("Invalid payload in Stripe webhook")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Неправильная подпись
        logger.exception("Invalid Stripe webhook signature")
        return HttpResponse(status=400)
    except Exception:
        logger.exception("Unexpected error while verifying Stripe webhook")
        return HttpResponse(status=400)

    # --- Обрабатываем полезные типы событий ---
    try:
        # ---------------- checkout.session.completed ----------------
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            customer_id = session.get("customer")  # stripe customer id
            subscription_id = session.get("subscription")  # id подписки (если подписка создана)
            client_reference_id = session.get("client_reference_id")
            email = session.get("customer_details", {}).get("email")

            profile = None
            # сначала пробуем найти профиль по client_reference_id (user.id)
            if client_reference_id:
                try:
                    profile = PublicProfile.objects.get(user_id=int(client_reference_id))
                except PublicProfile.DoesNotExist:
                    profile = None

            # если не нашли по client_reference_id — пробуем по email
            if profile is None and email:
                try:
                    profile = PublicProfile.objects.get(user__email=email)
                except PublicProfile.DoesNotExist:
                    profile = None

            # если нашли профиль — сохраняем данные
            if profile:
                profile.stripe_customer_id = customer_id or profile.stripe_customer_id
                profile.stripe_subscription_id = subscription_id or profile.stripe_subscription_id
                profile.is_active_subscription = True

                # определим тариф по price_id (берём line items из checkout session)
                try:
                    line_items = stripe.checkout.Session.list_line_items(session["id"], limit=1)
                    if line_items and len(line_items.data) > 0:
                        price_id = line_items.data[0].price.id
                        if price_id == settings.STRIPE_PRICE_PRO:
                            profile.plan = "pro"
                        elif price_id == settings.STRIPE_PRICE_PREMIUM:
                            profile.plan = "premium"
                except Exception:
                    logger.exception("Failed to list line items for session %s", session.get("id"))

                profile.save()

        # ---------------- customer.subscription.created ----------------
        elif event["type"] == "customer.subscription.created":
            subscription = event["data"]["object"]
            customer_id = subscription.get("customer")
            sub_id = subscription.get("id")

            try:
                profile = PublicProfile.objects.get(stripe_customer_id=customer_id)
                profile.stripe_subscription_id = sub_id
                profile.is_active_subscription = True
                # можно дополнительно смотреть subscription['items'] чтобы установить план
                profile.save()
            except PublicProfile.DoesNotExist:
                logger.info("Subscription created for unknown customer: %s", customer_id)

        # ---------------- invoice.paid ----------------
        elif event["type"] == "invoice.paid":
            invoice = event["data"]["object"]
            customer_id = invoice.get("customer")

            try:
                profile = PublicProfile.objects.get(stripe_customer_id=customer_id)
                profile.is_active_subscription = True
                profile.save()
            except PublicProfile.DoesNotExist:
                logger.info("Invoice paid for unknown customer: %s", customer_id)

        # ---------------- customer.subscription.deleted ----------------
        elif event["type"] == "customer.subscription.deleted":
            subscription = event["data"]["object"]
            customer_id = subscription.get("customer")

            try:
                profile = PublicProfile.objects.get(stripe_customer_id=customer_id)
                profile.is_active_subscription = False
                profile.plan = "free"
                profile.stripe_subscription_id = None
                profile.save()
            except PublicProfile.DoesNotExist:
                logger.info("Subscription deleted for unknown customer: %s", customer_id)

        else:
            # остальные события мы можем игнорировать или логировать
            logger.debug("Unhandled Stripe event type: %s", event["type"])

    except Exception:
        logger.exception("Error while processing Stripe webhook event")

    return HttpResponse(status=200)

def payment_success(request):
    session_id = request.GET.get('session_id')
    return render(request, 'payment/success.html', {"session_id":session_id})

def payment_cancel(request):
    return render(request, 'payment/cancel.html')

