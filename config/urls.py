from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static, settings

from payment.views import ClickWebhookAPIView

urlpatterns = [
	path('admin/', admin.site.urls),
	path('user/v2/', include('user.urls')),
	path('payment/v2/', include('payment.urls')),
	path('volunteer/v2/', include('volunteer.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
