import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SSLPayment
from sslcommerz.serializers import SSLPaymentSerializer
import uuid
from django.http import JsonResponse
from django.shortcuts import redirect
from django.http import Http404
from .models import SSLPayment

class InitiatePaymentView(APIView):
    def post(self, request):
        # Get payment data from the frontend
        amount = request.data.get('amount')
        reference = request.data.get('reference')
        cus_name = request.data.get('cus_name')
        cus_email = request.data.get('cus_email')
        cus_phone = request.data.get('cus_phone')
        cus_address = request.data.get('cus_address')
        cus_city = request.data.get('cus_city')
        cus_country = request.data.get('cus_country')
        currency = 'BDT'
        transaction_id = str(uuid.uuid4())

        # Store the payment in the database
        payment = SSLPayment.objects.create(
            transaction_id=transaction_id,
            amount=amount,
            currency=currency,
            status='PENDING',
            reference=reference,
            cus_name=cus_name,
            cus_email=cus_email,
            cus_phone=cus_phone,
            cus_address=cus_address,
            cus_city=cus_city,
            cus_country=cus_country,
        )
        # SSLCommerz payment initialization data
        payment_data = {
            'store_id': settings.SSLCOMMERZ_STORE_ID,
            'store_passwd': settings.SSLCOMMERZ_STORE_PASSWORD,
            'total_amount': amount,
            'currency': currency,
            'tran_id': transaction_id,
            'success_url': settings.SSLCOMMERZ_SUCCESS_URL,
            'fail_url': settings.SSLCOMMERZ_FAIL_URL,
            'cancel_url': settings.SSLCOMMERZ_CANCEL_URL,
            'cus_name': request.data.get('cus_name'),
            'cus_email': request.data.get('cus_email'),
            'cus_phone': request.data.get('cus_phone'),
            'cus_add1': request.data.get('cus_address'),
            'cus_city': request.data.get('cus_city'),
            'cus_country': request.data.get('cus_country'),
            'shipping_method': 'NO',
            'product_name': 'Test Product',
            'product_category': 'Test Category',
            'product_profile': 'general'
        }

        # Send request to SSLCommerz API
        response = requests.post(settings.SSLCOMMERZ_API_URL, data=payment_data)
        response_data = response.json()

        # Log the response data
        # logger.debug(f'SSLCommerz Response Data: {response_data}')

        if response_data.get('status') == 'SUCCESS':
            return Response({
                'status': 'SUCCESS',
                'payment_url': response_data['GatewayPageURL'],
            })
        else:
            payment.status = 'FAILED'
            payment.save()
            return Response({'status': 'FAILED', 'message': f'Payment initiation failed: {response_data}'}, status=status.HTTP_400_BAD_REQUEST)

class PaymentSuccessView(APIView):
    def post(self, request):
        transaction_id = request.data.get('tran_id')
        domain = 'localhost:3000'
        payment = SSLPayment.objects.get(transaction_id=transaction_id)
        # Validate payment with SSLCommerz
        validation_data = {
            'val_id': request.data.get('val_id'),
            'store_id': settings.SSLCOMMERZ_STORE_ID,
            'store_passwd': settings.SSLCOMMERZ_STORE_PASSWORD,
            'format': 'json',
        }

        validation_response = requests.get(settings.SSLCOMMERZ_VALIDATION_URL, params=validation_data)
        validation_data = validation_response.json()

        if validation_data['status'] == 'VALID':
            payment.status = 'SUCCESS'
            payment.save()
            redirect_url = f"http://{domain}/payments/success/?transaction_id={transaction_id}"
            return redirect(redirect_url)
        else:
            payment.status = 'FAILED'
            payment.save()
            return Response(
                {'status': 'FAILED', 'transaction_id': transaction_id, 'message': 'Payment validation failed'},
                status=status.HTTP_400_BAD_REQUEST)


# class PaymentFailView(APIView):
#     def post(self, request):
#         transaction_id = request.data.get('tran_id')
#         domain = 'localhost:3000'
#         payment = SSLPayment.objects.get(transaction_id=transaction_id)
#         payment.status = 'FAILED'
#         payment.save()
#         redirect_url = f"http://{domain}/payments/failed/?transaction_id={transaction_id}"
#         return redirect(redirect_url)
#         return Response({'status': 'FAILED', 'message': 'Payment failed for some reason'}, status=status.HTTP_400_BAD_REQUEST)
    class PaymentFailView(APIView):
        def post(self, request):
            transaction_id = request.data.get('tran_id')
            domain = 'localhost:3000'
            try:
                payment = SSLPayment.objects.get(transaction_id=transaction_id)
            except SSLPayment.DoesNotExist:
                raise Http404("Payment not found")
            payment.status = 'FAILED'
            payment.save()
            redirect_url = f"http://{domain}/payments/failed/?transaction_id={transaction_id}"
            return redirect(redirect_url)

class PaymentCancelView(APIView):
    def post(self, request):
        transaction_id = request.data.get('tran_id')
        domain = 'localhost:3000'
        try:
            payment = SSLPayment.objects.get(transaction_id=transaction_id)
        except SSLPayment.DoesNotExist:
            raise Http404("Payment not found")
        payment.status = 'FAILED'
        payment.save()
        redirect_url = f"http://{domain}/payments/cancel/?transaction_id={transaction_id}"
        return redirect(redirect_url)