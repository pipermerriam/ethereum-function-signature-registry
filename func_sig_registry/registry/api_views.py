from rest_framework import generics
from rest_framework import viewsets
from rest_framework import mixins

from .models import Signature
from .tasks import perform_github_import
from .filters import SignatureFilter
from .serializers import (
    SignatureSerializer,
    SolidityImportSerializer,
    ContractABISerializer,
    GithubWebhookSerializer,
)


class SignatureViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    queryset = Signature.objects.all().select_related('bytes_signature')
    serializer_class = SignatureSerializer
    filter_class = SignatureFilter


class SolidityImportAPIView(generics.CreateAPIView):
    serializer_class = SolidityImportSerializer


class ContractABIImportAPIView(generics.CreateAPIView):
    serializer_class = ContractABISerializer


class GithubPushWebhookAPIView(generics.CreateAPIView):
    serializer_class = GithubWebhookSerializer

    def perform_create(self, serializer):
        push_data = serializer.save()
        repository = push_data['repository']['name']
        username = push_data['repository']['owner']['name']
        commit = push_data['head_commit']['id']
        perform_github_import(repository, username, commit)
