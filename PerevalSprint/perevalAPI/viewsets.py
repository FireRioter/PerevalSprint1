from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response

from perevalAPI.serializers import *
from perevalAPI.models import *


class UsersViewset(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class CoordsViewset(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


class LevelViewset(viewsets.ModelViewSet):
    queryset = Levels.objects.all()
    serializer_class = LevelSerializer


class PerevalViewset(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer
    filterset_fields = ["user__email"]
    def create(self, request, *args, **kwargs):
        serializer = PerevalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": status.HTTP_200_OK,
                "massage": "OK",
                'id': serializer.data['id'],
            })
        if status.HTTP_400_BAD_REQUEST:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "massage": serializer.errors,
                "id": None,
            })
        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "massage": "Ошибка подключения к БД",
                "id": None,
            })

    def partial_update(self, request, *args, **kwargs):
        pereval = self.get_object()
        if pereval.status == "new":
            serializer = PerevalSerializer(pereval, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "state": "1",
                    "massage": "Запись изменена",
                })

            else:
                return Response({
                    "state": "0",
                    "massage": serializer.errors,
                })
        else:
            return Response({
                "state": "0",
                "massage": f"Отклонено. Причина {pereval.get_status_display()} ",
            })

class ImagesViewset(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImageSerializer