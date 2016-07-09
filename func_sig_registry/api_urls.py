from django.conf.urls import url

from rest_framework import routers

from func_sig_registry.registry.api_views import (
    SignatureViewSet,
    SolidityImportAPIView,
)


router = routers.SimpleRouter()
router.register(r'signatures', SignatureViewSet)

urlpatterns = [
    url(r'import-solidity/$', SolidityImportAPIView.as_view(), name='import-solidity'),
] + router.urls
