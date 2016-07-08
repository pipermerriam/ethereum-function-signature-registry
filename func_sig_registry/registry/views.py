from django.shortcuts import redirect
from django.views.generic import ListView

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from django_tables2 import SingleTableView

from .models import Signature
from .tables import SignatureTable
from .serializers import (
    SignatureSerializer,
    SolidityImportSerializer,
    SignatureSearchSerializer,
)
from .utils import (
    decode_hex,
    force_text,
)


class SignatureListView(SingleTableView, ListView):
    model = Signature
    table_class = SignatureTable
    table_pagination = {
        'per_page': 10
    }

    def get_queryset(self):
        queryset = super(SignatureListView, self).get_queryset()
        if self.request.GET.get('bytes4_signature'):
            hex_signature = self.request.GET['bytes4_signature']
            bytes4_signature = force_text(decode_hex(hex_signature))
            return queryset.filter(bytes_signature__bytes4_signature=bytes4_signature)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SignatureListView, self).get_context_data(**kwargs)
        if self.request.GET.get('bytes4_signature'):
            serializer = SignatureSearchSerializer(data=self.request.GET)
            serializer.is_valid()
        else:
            serializer = SignatureSearchSerializer()
        context['serializer'] = serializer
        return context


class SignatureCreateView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'registry/signature_create.html'
    serializer_class = SignatureSerializer

    def get(self, *args, **kwargs):
        serializer = self.get_serializer()
        return Response({
            'serializer': serializer,
        })

    def post(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save()
        return redirect('site-index')


class SolidityImportView(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'registry/solidity_source_import.html'
    serializer_class = SolidityImportSerializer

    def get(self, *args, **kwargs):
        serializer = self.get_serializer()
        return Response({
            'serializer': serializer,
        })

    def post(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        source_file = serializer.save()
        Signature.import_from_solidity_source(source_file)
        return redirect('site-index')
