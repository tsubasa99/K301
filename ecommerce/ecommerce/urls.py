from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from os import getenv

urlpatterns = [
    path(getenv('ADMIN_URL'), admin.site.urls),
    path('i18n/',include('django.conf.urls.i18n'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +i18n_patterns(
    path('',include('shop.urls')),
    path('customer/', include('customer.urls')),
    path('payment/', include('payment.urls')),

    
)
