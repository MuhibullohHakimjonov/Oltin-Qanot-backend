from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static, settings

from payment.views import ClickWebhookAPIView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
	path('admin/', admin.site.urls),
	path('user/v2/', include('user.urls')),
	path('payment/v2/', include('payment.urls')),
	path('volunteer/v2/', include('volunteer.urls')),
	path('custom_admin/v2/', include('custom_admin.urls')),

	path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
	# Optional UI:
	path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
	path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
