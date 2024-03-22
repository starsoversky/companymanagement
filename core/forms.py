from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

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
