from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser, FileUploadParser
from rest_framework import status


from .utils import send_otp,verify_otp
from .serializers import UserSerializer,RequestPassswordResetEmailSerializer,RiderSerializer,PassangerSerializier

from .utils import PasswordResetTokenGenerator,decode_user_id,send_password_reset_email,password_reset_token_is_valid

User = get_user_model()

# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

class SendOTP(APIView):
    def get(self,request,*args,**kwargs):

        user_id = request.query_params.get('user_id') # get request is made by sending user id to param
        user = User.objects.get(id = user_id)
        send_otp(user)

        return Response({"message":f"OTP sent to {user.email}", "user_id":f"{user.id}"})


class VerifyOTP(APIView):

    def post(self, request, *args, **kwargs): #post request made with json data user_id, add otp
    #    print(request.data)
       otp = request.data.get('otp',None)
       user_id = request.data.get('user_id',None)
       if  (otp == None):
           return Response({"message":"Provide OTP"})
       if  (user_id == None):
           return Response({"message":"Provide UserID"})
       user = User.objects.get(id=user_id)

       
       if verify_otp(user,otp):
           user.is_verified=True
           user.save()
           token = RefreshToken.for_user(user).access_token
           return Response(
                {
                    "token": str(token),
                    "user": UserSerializer(user).data,
                },
                status=201,
            )
       else:
           return Response(
               {"error":"Incorrect OTP"},status=400
               )
              
       

class Login(APIView):

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail": "You are already authenticated"}, status=400)

        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if not email or not password:
            return Response(
                {"error": "Please enter your email or password"}, status=400
            )

        try:
            obj = User.objects.get(email=email)
        except:
            return Response({"error": "Email not registered"}, status=401)

        if obj.check_password(password):
            user = obj
            token = RefreshToken.for_user(user).access_token

# 
            # if obj.user_type == 'rider':

            return Response(
                        {
                            "token": str(token),
                            "user": str(user),
                        },
                        status=201,
                    )
            # else:
            #     Response({"error":"Unknown user perhaps login the passenger site or create a rider acount"}, status=400)

     
        else:
            return Response({"error": "Invalid password"}, status=401)
        
class ResetPassword(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        user_id_encoded = request.data.get("user", None)
        token = request.data.get("token", None)
        password1 = request.data.get("password1", None)
        password2 = request.data.get("password2", None)

        # Check all request data are complete
        if not user_id_encoded or not token or not password1 or not password2:
            return Response(
                {"error": "Please provide all data"}, status=status.HTTP_400_BAD_REQUEST
            )

        if password1 != password2:
            return Response(
                {"error": "passwords don't match"}, status=status.HTTP_400_BAD_REQUEST
            )

        user_id = decode_user_id(user_id_encoded)
        if not user_id:
            return Response(
                {"error": "unable to identify user"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=user_id)
        except:
            return Response(
                {"error": "user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        if not password_reset_token_is_valid(user, token):
            return Response(
                {"error": "token not valid, please request a new one"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(password1)
        user.save()
        return Response(
            {"detail": "password successfully changed"}, status=status.HTTP_200_OK
        )
class PassengerLogin(APIView):

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail": "You are already authenticated"}, status=400)

        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if not email or not password:
            return Response(
                {"error": "Please enter your email or password"}, status=400)

        try:
            obj = User.objects.get(email=email)
        except:
            Response({"error": "Email not registered"}, status=401)

        if obj.check_password(password):
            user = obj
            token = RefreshToken.for_user(user).access_token
       
            if obj.user_type == 'passenger':

                return Response(
                        {
                            "token": str(token),
                            "user": str(user),
                        },
                        status=201,
                    )
            else:
                Response({"error":"Unknown user perhaps login the passenger site or create arider acount"}, status=400)
        else:
            return Response({"error": "Invalid password"}, status=401)


class ForgetPassword(APIView):
    def post(self, request):
    
    # print(request.data)
        serializer = RequestPassswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        
        user = User.objects.filter(email=email)
        if not user.exists():
            return Response(
                {"error": "user with this email does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = user.first()
        # acc = Account.objects.get(user = user)
      
        # server= settings.SERVER
        password_sent = send_password_reset_email(user, request)
        if password_sent:
            return Response(
                {"detail": "password reset link has been sent to your email"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Email not sent"}, status=status.HTTP_400_BAD_REQUEST
            )

# class RiderForgetPassword(APIView):
      
#     def post(self, request):
    
#     # print(request.data)
#         serializer = RequestPassswordResetEmailSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.data["email"]
        
#         user = User.objects.filter(email=email)
#         if not user.exists():
#             return Response(
#                 {"error": "user with this email does not exist"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         user = user.first()
#         # acc = Account.objects.get(user = user)
#         if not (user.user_type == 'rider'):
#             return Response(
#                 {"error": "rider with this email does not exist"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         # server= settings.SERVER
#         password_sent = send_password_reset_email(user, request)
#         if password_sent:
#             return Response(
#                 {"detail": "password reset link has been sent to your email"},
#                 status=status.HTTP_200_OK,
#             )
#         else:
#             return Response(
#                 {"error": "Email not sent"}, status=status.HTTP_400_BAD_REQUEST
#             )


class PassengerRegistration(CreateAPIView):
    # parser_classes = ( MultiPartParser, FormParser,JSONParser,FileUploadParser)
    serializer_class = PassangerSerializier

    def post(self, request, *args, **kwargs):
       
        return self.create(request, *args, **kwargs)


    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
 
        passenger_obj = serializer.save()
        user = passenger_obj.user

        otp = send_otp(user)
        user.otp = otp
        user.save()

        return {"message":f"OTP sent to {user.email}", "user_id":f"{user.id}"}
    
class RiderRegistration(CreateAPIView):
    parser_classes = ( MultiPartParser, FormParser,JSONParser,FileUploadParser)
    serializer_class = RiderSerializer

    def post(self, request, *args, **kwargs):
       
        return self.create(request, *args, **kwargs)


    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):

        rider = serializer.save()
        user = rider.user
        otp = send_otp(user)
        if otp:

            user.otp = otp
            user.save()

            return {"message":f"OTP sent to {user.email}", "user_id":f"{user.id}"}
        return {'error': f'Error occured while generating OTP for {user.email}'}

