from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('profiles/', include(('profiles.urls', 'profiles'), namespace='profiles')),
    path('payment/', include(('payment.urls', 'payment'), namespace='payment')),
    path('', include(('main.urls', 'main'), namespace='main')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                document_root=settings.MEDIA_ROOT)
