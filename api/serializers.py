import django.core.exceptions as django_exceptions
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.models import (
    Accident,
    AccidentBidding,
    CarRepairCompanyAgent,
    CarRepairCompanyOffer,
    CustomerUser,
    Vehicle,
)
from core.validator import (
    PasswordValidator,
    validate_fincode,
    validate_last_name,
    validate_person_name,
    validate_phone_number,
)

User = get_user_model()

from django.contrib.auth.password_validation import validate_password


class RegisterBaseSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(
    #     required=True, validators=[UniqueValidator(queryset=CustomerUser.objects.all())]
    # )

    # password = serializers.CharField(
    #     write_only=True, required=True, validators=[validate_password]
    # )

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
        return user


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


class AccidentSerializers(serializers.ModelSerializer):
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


class AccidentBiddingSerializers(serializers.ModelSerializer):
    class Meta:
        model = AccidentBidding
        fields = "__all__"


class OfferSerializers(serializers.ModelSerializer):
    class Meta:
        model = CarRepairCompanyOffer
        fields = "__all__"
