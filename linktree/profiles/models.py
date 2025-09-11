from django.db import models
from django.conf import settings

class PublicProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='public_profile')
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

class SocialLink(models.Model):
    profile = models.ForeignKey(PublicProfile, on_delete=models.CASCADE, related_name="social_links")
    name = models.CharField(max_length=50, verbose_name="Назва соцмережі")
    url = models.URLField(verbose_name="Посилання")

    class Meta:
        unique_together = ("profile", "name")

    def __str__(self):
        return f"{self.name} ({self.profile.user.username})"
    

class CustomButton(models.Model):
    profile = models.ForeignKey(PublicProfile, on_delete=models.CASCADE, related_name="custom_links")
    title = models.CharField(max_length=100, verbose_name="Назва")
    url = models.URLField(verbose_name="Посилання")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.title} ({self.profile.user.username})"
