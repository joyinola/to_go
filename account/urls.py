from django.urls import path
from .views import (
    VerifyOTP,
    SendOTP,
    Login,
    PassengerLogin,
    ForgetPassword,
    # PassengerForgetPassword,
    RiderRegistration,
    PassengerRegistration,
    ResetPassword)


urlpatterns =[
    path('verifyotp/', VerifyOTP.as_view(),name='verify-otp'),
    path('send_otp/', SendOTP.as_view(),name='send-otp'),
    path('login/',Login.as_view(), name = 'login'),
    # path('login/passenger/',PassengerLogin.as_view(), name = 'login'),
    path('forget_password/', ForgetPassword.as_view(),name="forget-password"),
    # path('forget_password/passenger/', PassengerForgetPassword.as_view(),name="forget-password"),
    path('reset_password/', ResetPassword.as_view(), name="reset-password"),
    # path('reset_password/', ResetPassword.as_view(), name="reset-password"),
    path('rider/register/',RiderRegistration.as_view(), name='register-rider'),

    path('passenger/register/',PassengerRegistration.as_view(), name='register-passenger'),
]

