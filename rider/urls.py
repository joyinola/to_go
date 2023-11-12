from django.urls import path
from .views import RiderRegistration,VerifyOTP,SendOTP,RiderLogin,ForgetPassword,ResetPassword

urlpatterns =[
    path('',RiderRegistration.as_view(), name='register-rider'),
    path('verifyotp/', VerifyOTP.as_view(),name='verify-otp'),
    path('send_otp/', SendOTP.as_view(),name='send-otp'),
    path('login/',RiderLogin.as_view(), name = 'login'),
    path('forget_password/', ForgetPassword.as_view(),name="forget-password"),
    path('reset_password/', ResetPassword.as_view(), name="reset-password"),
]