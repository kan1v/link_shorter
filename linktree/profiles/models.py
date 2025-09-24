from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid

class SubscriptionPlan(models.TextChoices):
    FREE = "free", "Безкоштовний"
    PRO = "pro", "Pro"
    PREMIUM = "premium", "Premium"

class PublicProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='public_profile')
    plan = models.CharField(
        max_length=20,
        choices=SubscriptionPlan.choices,
        default=SubscriptionPlan.FREE,
        verbose_name="Тариф"
    )
    qr_code = models.ImageField(upload_to="profile_qrcodes/",blank=True, null=True,verbose_name="QR-код профілю")
    background = models.ImageField(upload_to='profile_backgrounds/', blank=True, null=True, verbose_name='Фонове зоображення')
    background_color = models.CharField(max_length=20, default='#ffffff', verbose_name='Колір фону')
    button_style = models.CharField(max_length=50, choices=[
        ("rounded", "Закруглені"),
        ("square", "Прямі"),
        ("pill", "Таблетка"),
    ], default="rounded", verbose_name="Стиль кнопок"
    )
    text_color = models.CharField(max_length=20, default="#000000", verbose_name="Колір тексту")
    slug = models.SlugField(unique=True, verbose_name="URL-ім'я", help_text="Наприклад: yourname, буде доступно за /u/yourname/")    

    def __str__(self):
        return f"Публічний профіль {self.user.username}"    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username)
            slug = base_slug
            counter = 1
            while PublicProfile.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class SocialLink(models.Model):
    profile = models.ForeignKey(PublicProfile, on_delete=models.CASCADE, related_name="social_links")
    name = models.CharField(max_length=50, verbose_name="Назва соцмережі")
    url = models.URLField(verbose_name="Посилання")

    def save(self, *args, **kwargs):
        limits = {'free':2, 'pro':5, 'premium':20}
        if self.profile.social_links.count() >= limits[self.profile.plan]:
            raise ValueError("Досягнуто ліміту посилань для вашого тарифу")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.profile.user.username})"


class CustomButton(models.Model):
    profile = models.ForeignKey(PublicProfile, on_delete=models.CASCADE, related_name="custom_links")
    title = models.CharField(max_length=100, verbose_name="Назва")
    url = models.URLField(verbose_name="Посилання")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    def save(self, *args, **kwargs):
        limits = {'free':2, 'pro':5, 'premium':20}
        if self.profile.social_links.count() >= limits[self.profile.plan]:
            raise ValueError("Досягнуто ліміту посилань для вашого тарифу")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.title} ({self.profile.user.username})"

