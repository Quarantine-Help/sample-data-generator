from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from pacifier.serializers import DataPacifierSerializer


class DataPacifierAPIView(APIView):
    serializer_class = DataPacifierSerializer

    def post(self, request, *args, **kwargs):
        request_data = self.serializer_class(request.data).data
        return Response({"success": True})
