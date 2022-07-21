from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from rest_framework import status
from django.shortcuts import get_object_or_404
import random
import string

from .serializers import SignupSerializer, AdminCreateUser
from .models import CustomUser


def get_confirmation_code():
    length = 36
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


class SignupView(APIView):

    permission_classes = [AllowAny, ]

    def post(self, request):
        if request.user.is_anonymous:
            serializer = SignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get('email')
            confirmation_code = get_confirmation_code()
            send_mail(recipient_list=[email],
                      message=f'confirmation_code: {confirmation_code}',
                      subject='confirmation_code', from_email=None)
            serializer.save(confirmation_code=confirmation_code)
            return Response(serializer.validated_data,
                            status=status.HTTP_200_OK)
        elif request.user.is_admin() or request.user.is_staff or request.user.is_superuser:
            serializer = AdminCreateUser(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get('email')
            confirmation_code = get_confirmation_code()
            send_mail(recipient_list=[email],
                      message=f'confirmation_code: {confirmation_code}',
                      subject='confirmation_code', from_email=None)
            serializer.save(confirmation_code=confirmation_code)
            return Response(serializer.validated_data,
                            status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_423_LOCKED)


class ConfirmRegisteredView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        if ("username" or "confirmation_code") not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(CustomUser, username=request.data['username'])
        if request.data['confirmation_code'] == user.confirmation_code:
            user.is_active = True
            user.save()
            token = user.get_tokens_for_user()['access']
            return Response(token, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
