from django.shortcuts import render
from django.conf import settings
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout
from .serializers import LoginSerializer, UserSerializer
from rest_framework import views, generics, response, permissions, authentication
import usersapp.models as user_models
import posts.models as posts_models


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


class MyBasicAuthentication(BasicAuthentication):

    def authenticate(self, request):
        user, _ = super(MyBasicAuthentication, self).authenticate(request)
        login(request, user)
        return user, _


class AuthView(views.APIView):
    authentication_classes = (SessionAuthentication, MyBasicAuthentication)
    permission_classes = (IsAuthenticated,)


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return response.Response(UserSerializer(user).data)


class LogoutView(views.APIView):

    def post(self, request):
        logout(request)
        return response.Response()


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        user.backend = settings.AUTHENTICATION_BACKENDS[0]
        login(self.request, user)
