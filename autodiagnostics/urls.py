from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView  # Изменен импорт

urlpatterns = [
    path('', RedirectView.as_view(url='/vehicles/', permanent=False), name='home'),  # Изменена эта строка
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)