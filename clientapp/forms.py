from django import forms
from .models import *
from user.models import Userprofile


class changepasswordform(forms.ModelForm):
    class Meta:
        model=Userprofile
        fields=['username','password']

class ClientRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    second_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Client
        fields = ['phone_number', 'image', 'email', 'dob', 'gender', 'place', 'country', 'username', 'first_name', 'second_name', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Userprofile.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Client.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
class ClientRegistrationForm1(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model=Client
        fields=['phone_number','email','dob','gender','place','country']

        def clean_username(self):
            username = self.cleaned_data.get('username')
            if Userprofile.objects.filter(username=username).exists():
                raise forms.ValidationError("Username already exists")
            return username

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if Client.objects.filter(email=email).exists():
                raise forms.ValidationError("Email already exists")
            return email
class addplaceform(forms.ModelForm):
    class Meta:
        model=placevisited
        fields=['placename']

class addpostform(forms.ModelForm):
    class Meta:
        model=posts
        fields=['postcontent','postfile']
# class addgrouppostform(forms.ModelForm):
#     class Meta:
#         model=posts
#         fields=['groupid','postcontent','postfile']

class Addwandergroupform(forms.ModelForm):
    class Meta:
        model = Wandergroup
        exclude = ['user','status','is_active','created_at','updated_at']

class Addcommentform(forms.ModelForm):
    class Meta:
        model=Commentpost
        exclude = ['user','status','is_active','created_at','updated_at']

class ClientRegistrationForm2(forms.ModelForm):

    # first_name = forms.CharField(max_length=30, required=True)
    # second_name = forms.CharField(max_length=30, required=True)


    class Meta:
        model = Client
        # fields = ['image', 'dob', 'gender', 'place', 'country','first_name', 'second_name'  ]
        fields = ['image', 'dob', 'gender', 'place', 'country',]