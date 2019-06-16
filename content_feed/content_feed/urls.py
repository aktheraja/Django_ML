
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from content_api.views import ItemViewSet
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter()
router.register(r'test', ItemViewSet, base_name='test')

urlpatterns = [
url(r'^api/', include(router.urls)),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
