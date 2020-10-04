import http

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


from pacifier.data_generator import DataGenerator
from pacifier.data_poster import DataPoster
from pacifier.serializers import DataPacifierSerializer


class DataPacifierAPIView(APIView):
    serializer_class = DataPacifierSerializer

    def post(self, request, *args, **kwargs):
        request_data = self.serializer_class(request.data).data

        data_generator = DataGenerator(
            type=request_data.get("type", "AF"),
            latitude=request_data.get("position")["latitude"],
            longitude=request_data.get("position")["longitude"],
            amount=request_data.get("amount", 10),
        )
        dummy_data = data_generator.generate_dummy_data()
        data_poster = DataPoster(
            auth_key=request_data.get("authKey", ""),
            target=request_data.get("target", "staging"),
            data=dummy_data,
        )
        post_response = data_poster.post_to_target()
        return Response({"createdData": post_response}, status=http.HTTPStatus.OK)
