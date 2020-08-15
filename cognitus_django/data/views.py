import requests
import json
import coreapi

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.schemas import AutoSchema


from .models import Data
from .serializers import DataSerializer, PredictionSerializer


class DataSchema(AutoSchema):
    manual_fields = []  # common fields

    def get_manual_fields(self, path, method):
        custom_fields = []
        if method.lower() == "post":
            custom_fields = [
                coreapi.Field(
                    "text",
                    required=True,
                    location='form',
                    description='Text'
                ),
                coreapi.Field(
                    "label",
                    required=True,
                    location='form',
                    description='Label'
                ),
            ]
        return self._manual_fields + custom_fields


class PredictSchema(AutoSchema):
    manual_fields = []  # common fields

    def get_manual_fields(self, path, method):
        custom_fields = [
            coreapi.Field(
                "text",
                required=True,
                location='form',
                description='Text'
            ),
        ]
        return self._manual_fields + custom_fields




class DataList(APIView):
    schema = DataSchema()
    serializer_class = DataSerializer

    def get(self, request):
        datas = Data.objects.all()
        serializer = DataSerializer(datas, many=True).data
        return Response(serializer)

    def post(self, request, *args, **kwargs):
        
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DataDetail(APIView):
    def get_object(self, pk):
        try:
            return Data.objects.get(pk=pk)
        except Data.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = DataSerializer(data)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = DataSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        data = self.get_object(pk)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Prediction(APIView):
    """
    İlk olarak Train işlemi yapılmalıdır.
    """
    schema = PredictSchema()
    serializer_class = PredictionSerializer

    def post(self, request):
        print('data', request.data)
        text = request.data.get('text')
        print('text', text)
        if text:
            print(1)
            req = requests.post(
                'http://algorithm:5000/prediction', data={'text': text})
            print(req.status_code)
            print(req.text)
            if req.status_code == 200:
                label = req.json()['label']
                # burda kayt alınabilir
                # obj = Data.objects.get_or_create(
                #     text=text,
                #     label=label
                # )
                return Response(label)
        return Response('Not Text', status=status.HTTP_400_BAD_REQUEST)


class Train(APIView):
    """
    İlk olarak 3 den fazla veri kaydedilmelidir.
    """
    def post(self, request):
        req = requests.get('http://algorithm:5000/train')
        if req.status_code == 200:
            return Response('Başarılı')
        else:
            return Response(req.text)
