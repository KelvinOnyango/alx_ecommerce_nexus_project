from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema

class ProductMetricsView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve product metrics (admin).",
        responses={
            200: "Metrics retrieved successfully.",
            403: "Permission denied."
        }
    )
    def get(self, request):
        # Logic for retrieving product metrics
        return Response({"message": "Metrics retrieved successfully."}, status=status.HTTP_200_OK)

class UnifiedSearchView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Perform a unified search.",
        responses={
            200: "Search results retrieved successfully.",
            400: "Invalid input data."
        }
    )
    def get(self, request):
        # Logic for performing unified search
        return Response({"message": "Search results retrieved successfully."}, status=status.HTTP_200_OK)