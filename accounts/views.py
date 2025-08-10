from rest_framework import generics, permissions
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user.",
        request_body=UserSerializer,
        responses={
            201: "User successfully registered.",
            400: "Invalid input data."
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_description="Obtain JWT tokens for authentication.",
        responses={
            200: "Tokens successfully obtained.",
            401: "Invalid credentials."
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve the authenticated user's profile.",
        responses={
            200: UserSerializer,
            401: "Unauthorized."
        }
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update the authenticated user's profile.",
        request_body=UserSerializer,
        responses={
            200: "Profile updated successfully.",
            400: "Invalid input data.",
            401: "Unauthorized."
        }
    )
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Request a password reset.",
        request_body=UserSerializer,
        responses={
            200: "Password reset email sent successfully.",
            400: "Invalid input data."
        }
    )
    def post(self, request):
        # Logic to send password reset email
        return Response({"message": "Password reset email sent successfully."}, status=status.HTTP_200_OK)

class UserRetrieveUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve the authenticated user's profile.",
        responses={
            200: UserSerializer,
            401: "Unauthorized."
        }
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update the authenticated user's profile.",
        request_body=UserSerializer,
        responses={
            200: "Profile updated successfully.",
            400: "Invalid input data.",
            401: "Unauthorized."
        }
    )
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)