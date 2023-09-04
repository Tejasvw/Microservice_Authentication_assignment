from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.response import  Response
from rest_framework.decorators import api_view
from .models import customUser
from .serializers import UserSerializer,PasswordResetSerializer,AccountUpdateSerializer
from django.core.mail import send_mail
from django.conf import settings
import random
from rest_framework.views import APIView
from django.utils.crypto import get_random_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_otp.plugins.otp_totp.models import TOTPDevice
from twilio.rest import Client
from django.utils import timezone
import phonenumbers
from phonenumbers import NumberParseException
from django.shortcuts import get_object_or_404
from twilio.base.exceptions import TwilioException






# Create your views here.

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()


            otp=''.join(random.choices('0123456789', k=6))


            subject = "Email Verification OTP"
            message=f"Your OTP for email verification is: {otp}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list =[user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return Response({'message': 'User registered successfully. Check your email for OTP verification.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


@api_view(['POST'])
def password_reset_request(request):
        serializer=PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = customUser.objects.get(email=email)
            except customUser.DoesNotExist:
                user = None

            if user:
                token = urlsafe_base64_encode(force_bytes(user.pk))

                reset_link = f"http://yourdomain.com/reset-password/{token}/"
                send_mail(
             "Password Reset Request",
                    f"Click the following link to reset your password:{reset_link}",
                    "from@example.com",
                    [email],
                    fail_silently=False,

                )

                return Response({'message': 'Password reset email has been sent successfully.'},status=status.HTTP_200_OK)
            else:
                return Response({'error':'User not found.'},status=status.HTTP_404_NOT_FOUND)
        return Response({serializer.errors: 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

customUser = get_user_model()

@csrf_exempt
def send_otp(request):
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        if not phone_number:
            return JsonResponse({'message': 'Phone number is required.'}, status=400)

        try:
            parsed_phone_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed_phone_number):
                return JsonResponse({'message': 'Invalid phone number.'}, status=400)
        except NumberParseException:
            return JsonResponse({'message': 'Invalid phone number format.'}, status=400)

        try:
            user, created = customUser.objects.get_or_create(phone_number=phone_number)
            otp = get_random_string(length=6, allowed_chars='0123456789')
            user.otp = otp
            user.otp_valid_until = timezone.now() + timezone.timedelta(minutes=5)
            user.save()

            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            msg = client.messages.create(
                body=f"OTP is: {otp}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number,
            )

            return JsonResponse({'message': 'OTP has been sent successfully'}, status=200)
        except TwilioException as e:
            # Handle Twilio exceptions and log the error
            print(f"Twilio Exception: {str(e)}")
            return JsonResponse({'message': 'Failed to send OTP'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def verify_otp(request):
   if request.method =="POST":
       phone_number = request.POST.get('phone_number')
       otp= request.POST.get('otp')

       if not phone_number or not otp:
           return JsonResponse({'message':'Phone number and OTP are required.'})

       user = get_object_or_404(customUser, phone_number=phone_number)
       if user.otp != otp:
           return JsonResponse({'message':'Invalid OTP.'},status=400)

       if timezone.now() > user.otp_valid_until:
           return JsonResponse({'message':'OTP has been expired.'}, status=400)

       user.otp = None
       user.otp_valid_until=None
       user.save()


       authenticated_user = authenticate(request, username = user.username, password=user.password)
       login(request, authenticated_user)
       # stored_otp = cache.get(f'otp_{phone_number}')
       # if stored_otp and entered_otp == stored_otp:
       #   cache.delete(f'otp_{phone_number}')

       return JsonResponse({'message':'OTP verified successful'}, status=200)


class AccountUpdateViewSet(viewsets.ModelViewSet):
    serializer_class = AccountUpdateSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return customUser.objects.filter(id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        instance = self.get_object(),
        serializer= self.get_serializer(instance, data= request.data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)