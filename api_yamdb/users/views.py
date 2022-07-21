from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from rest_framework import status
from django.shortcuts import get_object_or_404
import random
import string

from .serializers import SignupSerializer
from .models import CustomUser


def get_confirmation_code():
    length = 36
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


class SignupView(APIView):

    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        confirmation_code = get_confirmation_code()
        send_mail(recipient_list=[email],
                  message=f'confirmation_code: {confirmation_code}',
                  subject='confirmation_code', from_email=None)
        serializer.save(confirmation_code=confirmation_code)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ConfirmRegisteredView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        User = get_object_or_404(CustomUser, username=request.data['username'])
        if request.data['confirmation_code'] == User.confirmation_code:
            User.is_active = True
            User.save()
            token = User.get_tokens_for_user()['access']
            return Response(token, status=status.HTTP_200_OK)
