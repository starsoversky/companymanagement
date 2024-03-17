from django.contrib.auth import authenticate, get_user_model
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

User = get_user_model()

from django.contrib.auth.password_validation import validate_password


class RegisterBaseSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=CustomerUser.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = (
            # "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "fin_code",
            "address",
            "phone_number",
            "user_type",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        email = value.lower()
        return email

    def save(self):
        """Serializer save, which pops unnecessary info from
        `validated_data` and creates user object

        :return: user object (defined in Meta subclass) with given data
        :rtype: MyUser
        """

        # Username = Email
        self.validated_data["username"] = self.validated_data["email"]
        user = self.Meta.model(**self.validated_data)
        user.is_active = False  # We did not eliminate is_active false for this reason ---https://stackoverflow.com/a/15122938/819982
        user.save()
        return user

    # def validate(self, attrs):
    #     if attrs["password"] != attrs["password2"]:
    #         raise serializers.ValidationError(
    #             {"password": "Password fields didn't match."}
    #         )

    #     return attrs

    # def create(self, validated_data):
    #     customer = CustomerUser.objects.create(
    #         user_type="C",
    #         username=validated_data["username"],
    #         email=validated_data["email"],
    #         first_name=validated_data["first_name"],
    #         last_name=validated_data["last_name"],
    #         fin_code=validated_data["fin_code"],
    #         address=validated_data["address"],
    #         phone_number=validated_data["phone_number"],
    #         is_active=False,
    #     )

    #     customer.set_password(validated_data["password"])
    #     customer.save()

    #     return customer


class CustomerRegisterSerializer(RegisterBaseSerializer):
    class Meta:
        model = CustomerUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
            "fin_code",
            "address",
            "phone_number",
            "user_type",
        )


class CarRepairCompanyAgentRegisterSerializer(RegisterBaseSerializer):
    class Meta:
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
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user:
            # and user.is_active and user.is_staff:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")


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


class AccidentBiddingSerializers(serializers.ModelSerializer):
    class Meta:
        model = AccidentBidding
        fields = "__all__"


class OfferSerializers(serializers.ModelSerializer):
    class Meta:
        model = CarRepairCompanyOffer
        fields = "__all__"
