from django.urls import path

from django.contrib import admin

from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
import WebAnalyzer.views


router = DefaultRouter()

router.register(r'image', WebAnalyzer.views.ImageViewSet)

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
