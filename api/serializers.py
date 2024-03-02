from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.models import Asset, Case, Competition, CustomerUser

User = get_user_model()

from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=CustomerUser.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = CustomerUser
        fields = (
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "fin_code",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    # def validate(self, attrs):
    #     if attrs["password"] != attrs["password2"]:
    #         raise serializers.ValidationError(
    #             {"password": "Password fields didn't match."}
    #         )

    #     return attrs

    def create(self, validated_data):
        customer = CustomerUser.objects.create(
            user_type="C",
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            fin_code=validated_data["fin_code"],
            is_active=False,
        )

        customer.set_password(validated_data["password"])
        customer.save()

        return customer


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


class AssetSerializers(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"


class CaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = "__all__"


class CompetitionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = "__all__"
