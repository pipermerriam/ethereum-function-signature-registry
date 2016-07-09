from rest_framework import viewsets
from rest_framework import mixins

from .models import Signature
from .filters import SignatureFilter
from .serializers import SignatureSerializer


class SignatureViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer
    filter_class = SignatureFilter
