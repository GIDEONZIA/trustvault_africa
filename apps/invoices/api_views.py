from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Invoice
from .serializers import InvoiceSerializer


class InvoiceListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = InvoiceSerializer
    filterset_fields = ['status', 'invoice_type']

    def get_queryset(self):
        user = self.request.user
        qs = Invoice.objects.select_related('lease', 'lease__tenant', 'lease__unit', 'lease__unit__building')
        if user.is_landlord:
            return qs.filter(lease__unit__building__owner=user)
        return qs.filter(lease__tenant=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Invoice created',
        }, status=status.HTTP_201_CREATED)


class InvoiceDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_landlord:
            return Invoice.objects.filter(lease__unit__building__owner=user)
        return Invoice.objects.filter(lease__tenant=user)


class InvoiceSendReminderAPIView(APIView):
    def post(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk, lease__unit__building__owner=request.user)
        except Invoice.DoesNotExist:
            return Response({'success': False, 'message': 'Invoice not found'}, status=404)

        invoice.reminder_count += 1
        invoice.save()
        return Response({
            'success': True,
            'message': 'Reminder sent',
        })


class InvoiceWaiveAPIView(APIView):
    def post(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk, lease__unit__building__owner=request.user)
        except Invoice.DoesNotExist:
            return Response({'success': False, 'message': 'Invoice not found'}, status=404)

        invoice.status = 'waived'
        invoice.save()
        return Response({
            'success': True,
            'data': InvoiceSerializer(invoice).data,
            'message': 'Invoice waived',
        })
