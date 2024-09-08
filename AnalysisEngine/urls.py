from django.urls import path

from django.contrib import admin

from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
import WebAnalyzer.views
from WebAnalyzer.views import ImageComparisonView

router = DefaultRouter()

router.register(r'image', WebAnalyzer.views.ImageViewSet)

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('results/', ImageComparisonView.as_view(), name='results'),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
