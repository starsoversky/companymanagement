from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_out
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Accident, AccidentBidding, CustomerUser, Vehicle

from .serializers import (
    AccidentBiddingSerializers,
    AccidentSerializers,
    LoginUserSerializer,
    RegisterSerializer,
    UserSerializer,
    VehicleSerializers,
)

User = get_user_model()


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


class RegisterView(generics.CreateAPIView):
    queryset = CustomerUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class VehicleListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = VehicleSerializers

    def get_queryset(self):
        qs = Vehicle.objects.filter(customer=self.request.user)
        return qs

    def create(self, request, *args, **kwargs):
        mutable_data = request.data.copy()
        mutable_data["customer"] = request.user.id
        mutable_data["customer_fin"] = request.user.fin_code
        # if request.user:
        #     asset_data["customer"] = request.user
        serializer = self.serializer_class(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccidentListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AccidentSerializers

    def get_queryset(self):
        qs = Accident.objects.filter(customer=self.request.user)
        return qs

    def create(self, request, *args, **kwargs):
        mutable_data = request.data.copy()
        mutable_data["customer"] = request.user.id
        # mutable_data["customer_fin"] = request.user.fin_code
        # if request.user:
        #     asset_data["customer"] = request.user
        serializer = self.serializer_class(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccidentBiddingListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AccidentBiddingSerializers

    def get_queryset(self):
        qs = AccidentBidding.objects.filter(customer=self.request.user)
        return qs

    def create(self, request, *args, **kwargs):
        mutable_data = request.data.copy()
        mutable_data["customer"] = request.user.id
        # mutable_data["customer_fin"] = request.user.fin_code
        # if request.user:
        #     asset_data["customer"] = request.user
        serializer = self.serializer_class(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
