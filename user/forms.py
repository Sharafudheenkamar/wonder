from .models import *
from django import  forms


class LoginForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ('first_name','second_name','username','password','user_type')