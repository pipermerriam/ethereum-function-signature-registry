from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import (
    ListView,
    TemplateView,
)

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from django_tables2 import SingleTableView

from func_sig_registry.utils.encoding import (
    remove_0x_prefix,
)
from func_sig_registry.utils.import_statistics import (
    retrieve_stats_from_import_results,
)

from .models import (
    Signature,
    EventSignature,
)
from .tables import (
    SignatureTable,
    EventSignatureTable,
)
from .forms import (
    AllSignatureCreateForm,
    SolidityImportForm,
    SignatureSearchForm,
    EventSignatureSearchForm,
    ContractABIForm,
)


class SiteIndexView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(SiteIndexView, self).get_context_data(**kwargs)
        context['serializer'] = SignatureSearchForm()
        context['total_signatures'] = Signature.objects.count()
        return context


class SignatureListView(SingleTableView, ListView):
    model = Signature
    table_class = SignatureTable
    table_pagination = {
        'per_page': 10
    }

    def get_queryset(self):
        queryset = super(SignatureListView, self).get_queryset().select_related(
            'bytes_signature',
        )
        if self.request.GET.get('bytes4_signature'):
            hex_signature = self.request.GET['bytes4_signature']
            unprefixed_hex_signature = remove_0x_prefix(hex_signature.lower())

            if len(unprefixed_hex_signature) == 8:
                return queryset.filter(
                    bytes_signature__hex_signature=unprefixed_hex_signature,
                )
            else:
                return queryset.filter(
                    bytes_signature__hex_signature__icontains=unprefixed_hex_signature,  # NOQA
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SignatureListView, self).get_context_data(**kwargs)
        if self.request.GET.get('bytes4_signature'):
            serializer = SignatureSearchForm(data=self.request.GET)
            serializer.is_valid()
        else:
            serializer = SignatureSearchForm()
        context['serializer'] = serializer
        return context


class EventSignatureListView(SingleTableView, ListView):
    model = EventSignature
    table_class = EventSignatureTable
    table_pagination = {
        'per_page': 10
    }

    def get_queryset(self):
        queryset = super(EventSignatureListView, self).get_queryset()

        if self.request.GET.get('bytes_signature'):
            hex_signature = self.request.GET['bytes_signature']
            unprefixed_hex_signature = remove_0x_prefix(hex_signature.lower())

            if len(unprefixed_hex_signature) == 64:
                return queryset.filter(
                    hex_signature=unprefixed_hex_signature,
                )
            else:
                return queryset.filter(
                    hex_signature__icontains=unprefixed_hex_signature,  # NOQA
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(EventSignatureListView, self).get_context_data(**kwargs)
        if self.request.GET.get('bytes_signature'):
            serializer = EventSignatureSearchForm(data=self.request.GET)
            serializer.is_valid()
        else:
            serializer = EventSignatureSearchForm()
        context['serializer'] = serializer
        return context


class SignatureCreateView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'registry/signature_create.html'
    serializer_class = AllSignatureCreateForm

    def compose_success_message(self, function_signature, event_signature):
        message_parts = []
        if function_signature is not None:
            signature, created = function_signature
            if created:
                message_parts.append('Added function signature {0}.'.format(
                    signature.text_signature,
                ))
        if event_signature is not None:
            signature, created = event_signature
            if created:
                message_parts.append('Added event signature {0}.'.format(
                    signature.text_signature,
                ))
        return ' '.join(message_parts)

    def compose_info_message(self, function_signature, event_signature):
        message_parts = []
        if function_signature is not None:
            signature, created = function_signature
            if not created:
                message_parts.append('Function signature {0} already exists.'.format(
                    signature.text_signature,
                ))
        if event_signature is not None:
            signature, created = event_signature
            if not created:
                message_parts.append('Event signature {0} already exists.'.format(
                    signature.text_signature,
                ))
        return ' '.join(message_parts)

    def any_signature_created(self, function_signature, event_signature):
        function_created = (function_signature is not None) and function_signature[1]
        event_created = (event_signature is not None) and event_signature[1]
        return function_created or event_created

    def get(self, *args, **kwargs):
        serializer = self.get_serializer()
        return Response({
            'serializer': serializer,
        })

    def post(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        try:
            if not serializer.is_valid():
                return Response({'serializer': serializer})
        except ValueError as e:
            messages.error(
                self.request._request,
                str(e)
            )
            return redirect('/submit')

        function_signature, event_signature = serializer.save()

        # Check if any signatures were created, otherwise notify the user
        # about existing signatures
        if self.any_signature_created(function_signature, event_signature):
            messages.success(
                self.request._request,
                self.compose_success_message(function_signature, event_signature)
            )
        else:
            messages.info(
                self.request._request,
                self.compose_info_message(function_signature, event_signature)
            )
        return redirect('signature-list')


class SolidityImportView(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'registry/solidity_source_import.html'
    serializer_class = SolidityImportForm

    def get(self, *args, **kwargs):
        serializer = self.get_serializer()
        return Response({
            'serializer': serializer,
        })

    def post(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        results = serializer.save()
        import_function_results = []
        import_event_results = []
        for file_obj in results['source_files']:
            import_function_results.extend(Signature.import_from_solidity_file(file_obj))
            import_event_results.extend(EventSignature.import_from_solidity_file(file_obj))

        stats_function = retrieve_stats_from_import_results(import_function_results)
        stats_event = retrieve_stats_from_import_results(import_event_results)

        num_processed = stats_function.num_processed + stats_event.num_processed
        num_imported = stats_function.num_imported + stats_event.num_imported
        num_duplicates = stats_function.num_duplicates + stats_event.num_duplicates
        num_ignored = stats_function.num_ignored + stats_event.num_ignored

        if num_processed == 0:
            messages.info(self.request._request, "No function or event signatures found")
        else:
            messages.success(
                self.request._request,
                "Found {0} function and event signatures.  Imported {1}, \
                    Ignored {2}, Skipped {3} duplicates.".format(
                    num_processed, num_imported, num_ignored, num_duplicates,
                ),
            )
        return redirect('signature-list')


class ImportContractABIView(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'registry/contract_abi_import.html'
    serializer_class = ContractABIForm

    def get(self, *args, **kwargs):
        serializer = self.get_serializer()
        return Response({
            'serializer': serializer,
        })

    def post(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        if not serializer.is_valid():
            return Response({
                'serializer': serializer,
                'serializer_errors': serializer.errors,
            })
        results = serializer.save()

        num_processed = results['num_processed']
        num_imported = results['num_imported']
        num_duplicates = results['num_duplicates']
        num_ignored = results['num_ignored']

        messages.success(
            self.request._request,
            "Found {0} function and event signatures.  \
                Imported {1}, Ignored {2}, Skipped {3} duplicates.".format(
                num_processed, num_imported, num_ignored, num_duplicates
            ),
        )
        return redirect('signature-list')
