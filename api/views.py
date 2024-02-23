from django.contrib.auth.signals import user_logged_out
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import UserCustomer

from .serializers import LoginUserSerializer, UserSerializer

# Create your views here.


# ---------------------------------------------------------------
class LoginView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        user_data = UserSerializer(user, context=self.get_serializer_context()).data
        response_data = {"user": user_data, "token": token}
        return Response(response_data, status=200)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request._auth.delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        return Response({"message": "Success"}, status=status.HTTP_200_OK)
