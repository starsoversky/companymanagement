from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_out
from django.db.models import Prefetch
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
    AgreementDocument,
    Appointment,
    CarRepairCompanyAgent,
    CarRepairCompanyOffer,
    CustomerUser,
    InsurancePolicy,
    OfferedServices,
    Vehicle,
)

from .serializers import (
    AccidentBiddingSerializers,
    AccidentSerializers,
    AgreementDocumentSerializers,
    AppointmentSerializer,
    CarRepairCompanyAgentRegisterSerializer,
    CustomerRegisterSerializer,
    InsurancePolicySerializer,
    LoginUserSerializer,
    OfferedServicesSerializer,
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


class OfferedServicesListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OfferedServicesSerializer
    queryset = OfferedServices.objects.all()


class VehicleListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = VehicleSerializers

    def get_queryset(self):
        qs = Vehicle.objects.filter(customer=self.request.user)
        return qs

    def create(self, request, *args, **kwargs):
        mutable_data = request.data.copy()  # Make a mutable copy of request.data
        mutable_data["customer"] = request.user.id
        mutable_data["customer_fin"] = request.user.fin_code
        serializer = self.serializer_class(data=mutable_data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VehicleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleSerializers
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        qs = Vehicle.objects.filter(customer=self.request.user)

        return qs

    def get(self, request, *args, **kwargs):
        try:
            vehicle = self.get_object()
            serializer = self.get_serializer(vehicle)
            return Response(serializer.data)
        except Vehicle.DoesNotExist:
            return Response(
                {"message": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            vehicle = self.get_object()
            serializer = self.get_serializer(vehicle, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Vehicle.DoesNotExist:
            return Response(
                {"message": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            vehicle = self.get_object()
            vehicle.delete()
            return Response(
                {"message": "Vehicle deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Vehicle.DoesNotExist:
            return Response(
                {"message": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND
            )


class AccidentListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AccidentSerializers

    def get_queryset(self):
        qs = Accident.objects.filter(customer=self.request.user)
        return qs

    def create(self, request, *args, **kwargs):
        mutable_data = request.data.copy()  # Make a mutable copy of request.data
        mutable_data["customer"] = request.user.id
        serializer = self.serializer_class(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccidentSerializers
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        qs = Accident.objects.filter(customer=self.request.user)
        return qs

    def get(self, request, *args, **kwargs):
        try:
            accident = self.get_object()
            serializer = self.get_serializer(accident)
            return Response(serializer.data)
        except Accident.DoesNotExist:
            return Response(
                {"message": "Accident not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            accident = self.get_object()
            serializer = self.get_serializer(accident, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Accident.DoesNotExist:
            return Response(
                {"message": "Accident not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            accident = self.get_object()
            accident.delete()
            return Response(
                {"message": "Accident deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Accident.DoesNotExist:
            return Response(
                {"message": "Accident not found"}, status=status.HTTP_404_NOT_FOUND
            )


class AccidentBiddingApiView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AccidentBiddingSerializers

    def get_queryset(self):
        if self.request.user.user_type == "2":
            qs = AccidentBidding.objects.prefetch_related(
                Prefetch(
                    "repair_offer",
                    queryset=CarRepairCompanyOffer.objects.filter(accepted_offer=True),
                )
            )
            return qs
        else:
            return ""


class OfferListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OfferSerializers

    def get_queryset(self):
        qs = CarRepairCompanyOffer.objects.filter(offer_owner=self.request.user.company)
        return qs

    def create(self, request, *args, **kwargs):
        mutable_data = request.data.copy()
        mutable_data["offer_owner_agent"] = request.user.id
        mutable_data["offer_owner"] = request.user.company
        # if request.user:
        #     asset_data["customer"] = request.user
        serializer = self.serializer_class(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OfferSerializers
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        qs = CarRepairCompanyOffer.objects.filter(offer_owner=self.request.user.company)
        return qs

    def get(self, request, *args, **kwargs):
        try:
            offer = self.get_object()
            serializer = self.get_serializer(offer)
            return Response(serializer.data)
        except CarRepairCompanyOffer.DoesNotExist:
            return Response(
                {"message": "Offer not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            offer = self.get_object()
            serializer = self.get_serializer(offer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except CarRepairCompanyOffer.DoesNotExist:
            return Response(
                {"message": "Offer not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            offer = self.get_object()
            offer.delete()
            return Response(
                {"message": "Offer deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except CarRepairCompanyOffer.DoesNotExist:
            return Response(
                {"message": "Offer not found"}, status=status.HTTP_404_NOT_FOUND
            )


class InsurancePolicyListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = InsurancePolicySerializer

    def get_queryset(self):
        queryset = InsurancePolicy.objects.filter(customer=self.request.user)
        return queryset


class AgreementDocumentListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AgreementDocumentSerializers

    def get_queryset(self):
        queryset = AgreementDocument.objects.filter(
            car_repair_company=self.request.user.company
        )
        return queryset


class AppointmentListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        queryset = Appointment.objects.filter(customer=self.request.user)
        return queryset
