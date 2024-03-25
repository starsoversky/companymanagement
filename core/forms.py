from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import validate_image_file_extension
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _

from core.models import Accident, CarRepairCompanyOffer

# get custom user
User = get_user_model()


class MyUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw şifrələr bazada saxlanmır, onları heç cürə görmək mümkün deyil "
            "bu istifadəçinin şifrəsidir, lakin siz onu dəyişə bilərsiziniz "
            ' <a href="../password/">bu form</a>. vasitəsilə'
        ),
    )

    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        # f = self.fields.get("user_permissions", None)
        # if f is not None:
        #     f.queryset = f.queryset.select_related("content_type")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


# class CarRepairCompanyOfferAdminForm(forms.ModelForm):
#     class Meta:
#         model = CarRepairCompanyOffer
#         fields = "__all__"

#     def init(self, *args, **kwargs):
#         super().init(*args, **kwargs)
#         # Override widget for accepted_offer and rejected_offer fields
#         self.fields["accepted_offer"].widget.attrs[
#             "onclick"
#         ] = "document.getElementById('id_rejected_offer').checked = false;"
#         self.fields["rejected_offer"].widget.attrs[
#             "onclick"
#         ] = "document.getElementById('id_accepted_offer').checked = false;"


# class AccidentAdminForm(forms.ModelForm):
#     class Meta:
#         model = Accident
#         fields = "__all__"

#     photos = forms.FileField(
#         widget=forms.ClearableFileInput(attrs={"multiple": True}),
#         label=_("Add photos"),
#         required=False,
#     )

#     def clean_photos(self):
#         """Make sure only images can be uploaded."""
#         for upload in self.files.getlist("photos"):
#             validate_image_file_extension(upload)

#     def save_photos(self, show):
#         """Process each uploaded image."""
#         for upload in self.files.getlist("photos"):
#             photo = Accident(show=show, photo=upload)
#             photo.save()
