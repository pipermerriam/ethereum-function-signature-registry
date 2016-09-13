import logging

from rest_framework import generics
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters

from .models import Signature
from .tasks import perform_github_import
from .filters import SignatureFilter
from .serializers import (
    SignatureSerializer,
    SolidityImportSerializer,
    ContractABISerializer,
    GithubWebhookSerializer,
)


logger = logging.getLogger()


class SignatureViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    queryset = Signature.objects.all().select_related('bytes_signature')
    serializer_class = SignatureSerializer
    filter_class = SignatureFilter
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('created_at',)


class SolidityImportAPIView(generics.CreateAPIView):
    serializer_class = SolidityImportSerializer


class ContractABIImportAPIView(generics.CreateAPIView):
    serializer_class = ContractABISerializer


class GithubPushWebhookAPIView(generics.CreateAPIView):
    serializer_class = GithubWebhookSerializer

    def perform_create(self, serializer):
        push_data = serializer.save()
        username = push_data['repository']['owner']['name']
        repository = push_data['repository']['name']
        commit = push_data['head_commit']['id']

        logger.info("Scheduling github fetch for %s/%s/%s", username, repository, commit)

        perform_github_import(username, repository, commit)
