from django.urls import path, include
from client.views import ClientViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'<client_id>', ClientViewSet)
router.register(r'', ClientViewSet)

urlpatterns = [
    path('', include(router.urls))
]
