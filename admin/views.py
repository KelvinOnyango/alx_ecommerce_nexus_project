from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema

class BulkUploadView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_description="Bulk upload product catalog (CSV/Excel).",
        responses={
            200: "Bulk upload successful.",
            400: "Invalid input data.",
            403: "Permission denied."
        }
    )
    def post(self, request):
        # Logic for bulk upload
        return Response({"message": "Bulk upload successful."}, status=status.HTTP_200_OK)

class PromotionManagementView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_description="Manage promotions.",
        responses={
            200: "Promotion management successful.",
            400: "Invalid input data.",
            403: "Permission denied."
        }
    )
    def post(self, request):
        # Logic for managing promotions
        return Response({"message": "Promotion management successful."}, status=status.HTTP_200_OK)

class CategoryManagementView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_description="Manage categories.",
        responses={
            200: "Category management successful.",
            400: "Invalid input data.",
            403: "Permission denied."
        }
    )
    def post(self, request):
        # Logic for managing categories
        return Response({"message": "Category management successful."}, status=status.HTTP_200_OK)

class UserManagementView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_description="Manage users.",
        responses={
            200: "User management successful.",
            400: "Invalid input data.",
            403: "Permission denied."
        }
    )
    def post(self, request):
        # Logic for managing users
        return Response({"message": "User management successful."}, status=status.HTTP_200_OK)