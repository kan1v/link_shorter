from django.contrib import admin
from .models import PublicProfile, SocialLink, CustomButton

class SocialLinksInline(admin.TabularInline):
    model = SocialLink
    extra = 0
    fields = ('name', 'url')
    can_delete = True

class CustomButtonInline(admin.TabularInline):
    model = CustomButton
    extra = 0
    fields = ('title', 'url')
    can_delete = True

@admin.register(PublicProfile)
class PublicProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug','qr_code', 'background', 'background_color',
                    'button_style', 'text_color', 'plan', 'stripe_customer_id', 'stripe_subscription_id', 'is_active_subscription')
    list_filter = ('user', 'slug', 'plan')
    search_fields = ('user', 'slug')
    inlines = [SocialLinksInline, CustomButtonInline]

    fieldsets = (
        ('Информация о пользователе',{
            'fields': ('user','plan' ,'slug','qr_code', 'background', 'background_color',
                    'button_style', 'text_color', 'stripe_customer_id', 'stripe_subscription_id', 'is_active_subscription')
        }),

    )
    
