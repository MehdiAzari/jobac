from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from .serializers import EmployerSerializer, FreelancerSerializer, UserSerializer
from .models import User, Freelancer, Employer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


class SignUpFreelancerView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = Freelancer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = Freelancer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            # response_data = {}
            # response_data.update(serializer.data)
            # response_data['user']['token'] = serializer.token
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class SignUpEmployerView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmployerSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = EmployerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            # response_data = {}
            # response_data.update(serializer.data)
            # response_data['user']['token'] = serializer.token
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class EditProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        if self.request.user.user_group == 2:
            return self.request.user.employer
        elif self.request.user.user_group == 3:
            return self.request.user.freelancer

    def get_serializer_class(self):
        if self.request.user.user_group == 1:
            return EmployerSerializer
        elif self.request.user.user_group == 2:
            return Freelancer
