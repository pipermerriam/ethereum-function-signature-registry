from django.conf.urls import url

from rest_framework import routers

from func_sig_registry.registry.api_views import (
    SignatureViewSet,
    SolidityImportAPIView,
    ContractABIImportAPIView,
    GithubPushWebhookAPIView,
)


router = routers.SimpleRouter()
router.register(r'signatures', SignatureViewSet)

urlpatterns = [
    url(r'import-solidity/$', SolidityImportAPIView.as_view(), name='import-solidity'),
    url(r'import-abi/$', ContractABIImportAPIView.as_view(), name='import-abi'),
    url(r'receive-github-webhook/$', GithubPushWebhookAPIView.as_view(), name='github-webhook'),
] + router.urls
