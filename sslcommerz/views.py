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
from mailing.models import SystemMailManager
from users.models import User
from django.template.loader import render_to_string
from django.core.mail import send_mail
import logging


logger = logging.getLogger(__name__)
class InitiatePaymentView(APIView):
    def post(self, request):
        # Get payment data from the frontend
        # print("Request Datass:", request.data)
        # print("tran id:",request.data.get('tran_id') )
        # raise Exception("Stopping execution for debugging")
        amount = request.data.get('amount')
        reference = request.data.get('reference')
        cus_name = request.data.get('cus_name')
        cus_email = request.data.get('cus_email')
        cus_phone = request.data.get('cus_phone')
        cus_address = request.data.get('cus_address')
        cus_city = request.data.get('cus_city')
        cus_country = request.data.get('cus_country')
        currency = 'BDT'
        # transaction_id = str(uuid.uuid4())
        transaction_id = request.data.get('tran_id')
        membershipId = request.data.get('membershipId')
        user_id = request.data.get('user_id')
          # check if membership id already exists
        existing_payment = SSLPayment.objects.filter(user_id=user_id).first()
        if existing_payment:

            membershipId = existing_payment.membershipId
        else:
            if not membershipId:
                membershipId = request.data.get('membershipId')
        # Store the payment in the database
        payment = SSLPayment.objects.create(
            transaction_id=transaction_id,
            # user_id=user_id,
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
            membershipId=membershipId,
            user_id=user_id,
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

# class PaymentSuccessView(APIView):
#     def post(self, request):
#         transaction_id = request.data.get('tran_id')
#         domain = 'localhost:3000'
#         payment = SSLPayment.objects.get(transaction_id=transaction_id)
#         # Validate payment with SSLCommerz
#         validation_data = {
#             'val_id': request.data.get('val_id'),
#             'store_id': settings.SSLCOMMERZ_STORE_ID,
#             'store_passwd': settings.SSLCOMMERZ_STORE_PASSWORD,
#             'format': 'json',
#         }

#         validation_response = requests.get(settings.SSLCOMMERZ_VALIDATION_URL, params=validation_data)
#         validation_data = validation_response.json()

#         if validation_data['status'] == 'VALID':
#             payment.status = 'SUCCESS'
#             payment.save()
#             redirect_url = f"http://{domain}/payments/success/?transaction_id={transaction_id}"
#             return redirect(redirect_url)
#         else:
#             payment.status = 'FAILED'
#             payment.save()
#             return Response(
#                 {'status': 'FAILED', 'transaction_id': transaction_id, 'message': 'Payment validation failed'},
#                 status=status.HTTP_400_BAD_REQUEST)
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

            email_address = payment.cus_email
            name = payment.cus_name
            membershipId = payment.membershipId
            transaction_id = payment.transaction_id
            # print(email_address)  
            mail_manager = SystemMailManager()
            sender = User.objects.filter(role='GS').first()
            recipients = [payment.cus_email]
            subject = 'Your Payment was Successful'
            context = {
                'name': name,   
                'membershipId': membershipId,   
                'transaction_id': transaction_id,   
            }
            body = render_to_string('payment_success.html', context)

            try:
                mail_manager.create_and_send_mail(sender, recipients, subject, body)
            except Exception as e:
                # Log the error but continue with the response
                logger.error(f"Failed to send payment success email: {str(e)}", exc_info=True)

            redirect_url = f"http://{domain}/payments/success/?transaction_id={transaction_id}"
            return redirect(redirect_url)
        else:
            payment.status = 'FAILED'
            payment.save()
            return Response(
                {'status': 'FAILED', 'transaction_id': transaction_id, 'message': 'Payment validation failed'},
                status=status.HTTP_400_BAD_REQUEST
            )


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

class PaymentUsers(APIView):
    def get(self, request):
        # Retrieve selected fields from SSLPayment objects
        payments = SSLPayment.objects.filter(status='SUCCESS').values(
              'cus_name',
              'cus_email',
              'membershipId',
              'transaction_id',
              'amount',
              'created_at',
              'cus_phone',
              'status',
              'cus_phone',
          )

        # print(list(payments))
        # Return data as JSON response
        return Response(list(payments), status=status.HTTP_200_OK)
       