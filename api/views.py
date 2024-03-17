from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_out
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from core.models import (
    Accident,
    AccidentBidding,
    CarRepairCompanyAgent,
    CarRepairCompanyOffer,
    CustomerUser,
    Vehicle,
)

from .serializers import (
    AccidentBiddingSerializers,
    AccidentSerializers,
    CarRepairCompanyAgentRegisterSerializer,
    CustomerRegisterSerializer,
    LoginUserSerializer,
    OfferSerializers,
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
    serializer_classes = {
        "1": CustomerRegisterSerializer,
        "2": CarRepairCompanyAgentRegisterSerializer,
    }

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_serializer_class(self, *args, **kwargs):
        register_type = self.request.data.get("user_type", "1")

        serializer_class = self.serializer_classes.get(
            register_type,
            CustomerRegisterSerializer,
        )

        return serializer_class


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


class AccidentBiddingApiView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AccidentBiddingSerializers

    def get_queryset(self):
        qs = AccidentBidding.objects.filter()
        return qs


class OfferListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OfferSerializers

    def get_queryset(self):
        qs = CarRepairCompanyOffer.objects.filter(offer_owner_agent=self.request.user)
        return qs

    def create(self, request, *args, **kwargs):
        mutable_data = request.data.copy()
        mutable_data["offer_owner_agent"] = request.user.id
        mutable_data["offer_owner"] = request.user
        breakpoint()
        # if request.user:
        #     asset_data["customer"] = request.user
        serializer = self.serializer_class(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
