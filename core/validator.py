import re

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers

# from base_user.utils.helpers import (
#     fincode_is_duplicate,
#     fincode_is_valid,
#     govid_is_valid,
# )

User = get_user_model()


class PasswordValidator:
    def call(self, value):
        # Regular expression to check if the password contains at least one digit, one uppercase letter, and one special character
        if not re.match(r"^(?=.*\d)(?=.*[A-Z])(?=.*[!@#$%/^&*()_+{}|:<>?]).*$", value):
            raise serializers.ValidationError(
                "Password must include numbers, uppercase letters, and special characters."
            )


def validate_person_name(name, validation_err_key=None):
    """Helper function for validating person name, which
    should not contain any non-ascii characters and numbers

    :param value: First/Last/Full Name of person
    :type value: str
    :raises serializers.ValidationError: If not valid name
    :return: Last name itself, if valid
    :rtype: str
    """

    exceptions = []

    if validation_err_key:
        validatation_errors = {validation_err_key: exceptions}
    else:
        validatation_errors = exceptions

    isascii = lambda s: len(s) == len(s.encode())
    if not isascii(name):
        exceptions.append(_("But English letters are allowed."))

    if any(map(str.isdigit, name)):
        exceptions.append(_("First name can only contain letters."))

    if exceptions:
        raise serializers.ValidationError(validatation_errors)

    return name


def validate_last_name(name, validation_err_key=None):
    """Helper function for validating person name, which
    should not contain any non-ascii characters and numbers

    :param value: First/Last/Full Name of person
    :type value: str
    :raises serializers.ValidationError: If not valid name
    :return: Last name itself, if valid
    :rtype: str
    """

    exceptions = []

    if validation_err_key:
        validatation_errors = {validation_err_key: exceptions}
    else:
        validatation_errors = exceptions

    isascii = lambda s: len(s) == len(s.encode())
    if not isascii(name):
        exceptions.append(_("But English letters are allowed."))

    if any(map(str.isdigit, name)):
        exceptions.append(_("Last name can only contain letters."))

    if exceptions:
        raise serializers.ValidationError(validatation_errors)

    return name


def fincode_is_valid(fin_code):
    fin_code_regex = r"^[0-9a-zA-Z]{7}$"
    return bool(re.match(fin_code_regex, fin_code))


def validate_fincode(validated_data):
    fin_code = validated_data
    if not fincode_is_valid(fin_code):
        raise serializers.ValidationError(_("Please enter a valid FIN."))
    return fin_code


def validate_phone_number(phone_number, validation_err_key=None):
    """Validation of phone number

    :param value: Phone number
    :type value: str
    :raises serializers.ValidationError: If number is not valid,\
        corresponding message with exception is returned.
    :return: Phone number, if valid
    :rtype: str
    """

    exceptions = []

    if validation_err_key:
        validatation_errors = {validation_err_key: exceptions}
    else:
        validatation_errors = exceptions

    if not phone_number.isdecimal():
        exceptions.append(_("Please enter a valid phone number."))

    if len(phone_number) != 7:
        exceptions.append(_("The number must be 7 in length"))

    if phone_number.startswith(("0", "1")):
        exceptions.append(_("The number cannot start with 0 or 1"))

    if exceptions:
        raise serializers.ValidationError(validatation_errors)

    return phone_number
