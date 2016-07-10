from rest_framework import generics
from rest_framework import viewsets
from rest_framework import mixins

from .models import Signature
from .filters import SignatureFilter
from .serializers import (
    SignatureSerializer,
    SolidityImportSerializer,
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
