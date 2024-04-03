import django.core.exceptions as django_exceptions
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers

from core.models import (
    Accident,
    AccidentBidding,
    AccidentPhoto,
    AgreementDocument,
    Appointment,
    CarRepairCompanyAgent,
    CarRepairCompanyOffer,
    CustomerUser,
    InsurancePolicy,
    OfferedServices,
    Vehicle,
)
from core.validator import (
    PasswordValidator,
    validate_fincode,
    validate_last_name,
    validate_person_name,
    validate_phone_number,
    validate_phone_prefix,
)

User = get_user_model()

from django.contrib.auth.password_validation import validate_password


class RegisterBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerUser
        fields = (
            # "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "fin_code",
            "address",
            "phone_prefix",
            "phone_number",
            "user_type",
            "registration_number",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "error_messages": {"required": "Email address is required."},
                "allow_null": False,
            },
            "email": {
                "error_messages": {
                    "invalid": "Please enter a valid email address, including ‘@’ and a proper domain extension."
                }
            },
            "first_name": {
                "required": True,
                "error_messages": {"required": "First name is required."},
                "allow_null": False,
            },
            "last_name": {
                "required": True,
                "error_messages": {"required": "Last name is required."},
                "allow_null": False,
            },
            "password": {
                "required": True,
                "error_messages": {"required": "Password is required."},
                "allow_null": False,
            },
            "fin_code": {
                "required": True,
                "error_messages": {
                    "required": "FIN (Fərdi İdentifikasiya Nömrəsi) is required."
                },
                "allow_null": False,
            },
            "address": {
                "required": True,
                "error_messages": {"required": "Address is required."},
                "allow_null": False,
            },
            "phone_number": {
                "required": True,
                "error_messages": {"required": "Phone number is required."},
                "allow_null": False,
            },
            "user_type": {
                "required": True,
                "error_messages": {"required": "Please select a user type."},
                "allow_null": False,
            },
        }

    def __init__(self, *args, **kwargs):
        super(RegisterBaseSerializer, self).__init__(*args, **kwargs)

        self.fields["email"].error_messages["invalid"] = "My custom required msg"

    def validate_first_name(self, value: str) -> str:
        """Validate first name, should not contain
        non-ascii characters and numbers

        :param value: First name of user
        :type value: str
        :raises serializers.ValidationError: If not valid name
        :return: First name itself, if valid
        :rtype: str
        """
        return validate_person_name(value)

    def validate_last_name(self, value: str) -> str:
        """Validate first name, should not contain
        non-ascii characters and numbers

        :param value: First name of user
        :type value: str
        :raises serializers.ValidationError: If not valid name
        :return: First name itself, if valid
        :rtype: str
        """
        return validate_last_name(value)

    def validate_fin_code(self, fin_code):
        """Validate first name, should not contain
        non-ascii characters and numbers

        :param value: First name of user
        :type value: str
        :raises serializers.ValidationError: If not valid name
        :return: First name itself, if valid
        :rtype: str
        """
        return validate_fincode(fin_code)

    def validate_password(self, password):
        PasswordValidator.call(self, password)
        try:
            validate_password(password)
        except django_exceptions.ValidationError:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long"
            )

        return password

    def validate_phone_number(self, phone_number):
        return validate_phone_number(phone_number)

    def validate_phone_prefix(self, phone_prefix):
        return validate_phone_prefix(phone_prefix)

    def save(self):
        """Serializer save, which pops unnecessary info from
        validated_data and creates user object

        :return: user object (defined in Meta subclass) with given data
        :rtype: MyUser
        """

        # Username = Email
        self.validated_data["username"] = self.validated_data["email"]
        self.validated_data["password"] = make_password(
            self.validated_data["password"]
        )  # Hash the password
        user = self.Meta.model(**self.validated_data)
        user.is_active = False  # We did not eliminate is_active false for this reason ---https://stackoverflow.com/a/15122938/819982
        user.save()
        # Generate email confirmation token
        token = default_token_generator.make_token(user)

        # Send confirmation email
        self.send_confirmation_email(user, token)
        return user

    def send_confirmation_email(self, user, token):
        current_site = get_current_site(self.context["request"])
        domain = current_site.domain
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        subject = "Activate your account"
        message = render_to_string(
            "confirmation_email.html",
            {
                "user": user,
                "domain": domain,
                "uid": uid,
                "token": token,
            },
        )

        email = EmailMessage(
            subject=subject,
            body=message,  # HTML content
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],
        )
        email.content_subtype = "html"  # Set content type to HTML
        email.send()


class CustomerRegisterSerializer(RegisterBaseSerializer):
    class Meta(RegisterBaseSerializer.Meta):
        pass


class CarRepairCompanyAgentRegisterSerializer(RegisterBaseSerializer):
    class Meta(RegisterBaseSerializer.Meta):
        model = CarRepairCompanyAgent
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
            "fin_code",
            "address",
            "phone_number",
            "phone_prefix",
            "user_type",
            "registration_number",
        )
        extra_kwargs = {
            "registration_number": {
                "required": True,
                "allow_null": False,
            },
        }


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "Please enter your email address.",
            "invalid": "Please enter a valid email address.",
        },
    )
    password = serializers.CharField(
        required=True,
        error_messages={
            "required": "Please enter your password.",
            "invalid": "Please enter a valid email address.",
        },
    )

    class Meta:
        extra_kwargs = {
            "email": {
                "required": True,
                "error_messages": {"required": "Please enter your email address."},
                "allow_null": False,
            },
            "password": {"write_only": True},
            "invalid": "Please enter a valid email address.",
        }

    def validate_email(self, value):
        email = value.lower()
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "The email address you entered does not match our records."
            )
        if User.objects.filter(email=email, is_active=False).exists():
            raise serializers.ValidationError(
                "Your account is not active. Please check your email for the activation notification or contact your insurance provider."
            )

        return email

    def validate(self, data):
        user = authenticate(**data)
        if user:
            # and user.is_active and user.is_staff:
            return user
        raise serializers.ValidationError("The password you entered is incorrect.")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
        )


class OfferedServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferedServices
        fields = "__all__"


class VehicleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = (
            "customer",
            "customer_fin",
            "insurance_policy",
            "make",
            "model",
            "year",
            "color",
            "type",
            "seating_capacity",
            "engine",
            "body",
            "plate_number",
            "vin",
        )


class AccidentPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccidentPhoto
        fields = ("id", "photo")


class AccidentSerializers(serializers.ModelSerializer):
    photos = serializers.ListField(child=serializers.ImageField(), write_only=True)

    class Meta:
        model = Accident
        fields = (
            "customer",
            "insurance_policy",
            "accident_date",
            "accident_time",
            "location",
            "description",
            "photos",
        )
        extra_kwargs = {
            "insurance_policy": {
                "required": True,
                "error_messages": {
                    "required": "Please enter your insurance policy number."
                },
                "allow_null": False,
            },
            "accident_date": {
                "required": True,
                "error_messages": {"required": "Please provide the accident date."},
                "allow_null": False,
            },
            "accident_time": {
                "required": True,
                "error_messages": {
                    "required": "Please enter the time of the accident."
                },
                "allow_null": False,
            },
            "location": {
                "required": True,
                "error_messages": {
                    "required": "Please enter the location of the accident."
                },
                "allow_null": False,
            },
            "description": {
                "required": True,
                "error_messages": {
                    "required": "Please provide a description of the accident."
                },
                "allow_null": False,
            },
            "photos": {
                "required": True,
                "error_messages": {
                    "required": "The photo could not be uploaded. Please try again."
                },
                "allow_null": False,
            },
        }

    def validate_location(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "The location provided is too short. Please provide more details."
            )
        return value

    def validate_description(self, value):
        if len(value) < 100:
            raise serializers.ValidationError(
                "he description is too brief. Please provide more details about the accident."
            )
        return value

    def validate_accident_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError(
                "The accident date cannot be in the future. Please enter a valid date."
            )
        return value

    def create(self, validated_data):
        photos_data = validated_data.pop("photos", [])
        accident = Accident.objects.create(**validated_data)

        for photo_data in photos_data:
            AccidentPhoto.objects.create(accident=accident, photos=photo_data)
        return accident


class InsurancePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurancePolicy
        fields = "__all__"


class AccidentBiddingSerializers(serializers.ModelSerializer):
    class Meta:
        model = AccidentBidding
        fields = "__all__"


class AgreementDocumentSerializers(serializers.ModelSerializer):
    class Meta:
        model = AgreementDocument
        fields = "__all__"


class OfferSerializers(serializers.ModelSerializer):
    services_to_provide = serializers.PrimaryKeyRelatedField(
        queryset=OfferedServices.objects.all(), many=True
    )

    class Meta:
        model = CarRepairCompanyOffer
        fields = "__all__"

    def validate(self, data):
        # Get the accident bidding from the data
        accident_bidding = data.get("accident_bidding")

        # Check if there is an existing offer for the same accident bidding
        existing_offer = CarRepairCompanyOffer.objects.filter(
            accident_bidding=accident_bidding
        ).exists()
        if existing_offer:
            raise serializers.ValidationError(
                "An offer already exists for this accident bidding."
            )

        return data


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"
