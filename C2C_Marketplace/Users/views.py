from rest_framework.response import Response
# from rest_framework.views import APIView 
from .serializers import LoginSerializer, RegisterSerializer, ResetPasswordSerializer, UpdateUserSerializer
from .models import CustomUser
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.utils import timezone


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Override create to return token after registration"""
        response = super().create(request, *args, **kwargs)
        user = CustomUser.objects.get(username=response.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        response.headers['Authorization'] = f"Token {token.key}"        
        response.cookies['Authorization'] = f"Token {token.key}"
        return response


class LoginView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        # CustomUser.objects.get(id=user.id).__setattr__(name='last_login',value=f'{timezone.now()}')
        # user.last_login = timezone.now()
        return Response(
            {
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                }
            },
            status=status.HTTP_200_OK
        )

class ForgetPasswordView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
            # Here you would typically send an email with a password reset link
            # For demonstration, we'll just return a success message
            return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
class LogoutView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return Response(
                {"error": "User is not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            token_key = auth_header.split(" ")[1]
            token = Token.objects.get(key=token_key)

            # token.delete()

            return Response(
                {"message": "Successfully logged out."},
                status=status.HTTP_200_OK
            )

        except (IndexError, Token.DoesNotExist):
            return Response(
                {"error": "Invalid token."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        


class ResetPasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResetPasswordSerializer
    
    def get_queryset(self):
        # Return queryset limited to the authenticated user
        user = getattr(self.request, "user", None)
        if user and user.is_authenticated:
            return CustomUser.objects.filter(id=user.id)
        return CustomUser.objects.none()

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user

        if not user or not user.is_authenticated:
            return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        user.set_password(serializer.validated_data.get("password"))
        user.save()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        
class UpdateUserView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserSerializer  # You might want to create a separate serializer for updates
    # permission_classes = [AllowAny]  # Adjust permissions as needed
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        return Response(
            {
                "message": "User updated successfully.",
                "data": response.data
            },
            status=status.HTTP_200_OK
        )
    
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)

        return Response(
            {
                "message": "User updated successfully.",
                "data": response.data
            },
            status=status.HTTP_200_OK
        )