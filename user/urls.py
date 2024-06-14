from django.urls import path
from .views import *


urlpatterns = [
    path('loadadmin/', Adminhomeload.as_view(), name='loadadmin'),
    path('loadclient/', Clienthomeload.as_view(), name='loadclient'),
    path('', UserLogin.as_view(), name='userlogin'),
    path('userlogout/',UserLogout.as_view(),name='userlogout'),
    path('forgotpassword/', ForgotPassword.as_view(), name='forgotpassword'),
    ]