# rooms/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room, Reservation
from .serializer import RoomSerializer, RoomeReservationSerilizer, APIResponse
from drf_spectacular.utils import extend_schema
from rest_framework import serializers

from .parameters import (
    Room_parameters,
    Roome_reservation_parameters,
    CheckReservedByDate_Parameters,
    CheckReservedByPeriod_Parameters,
)
from .models import Room


class RoomCreateAPIView(APIView):
    @extend_schema(
        request={
            "application/json": Room_parameters,
        }
    )
    def post(self, request):
        try:
            room = Room.create(request.data)
            data = RoomSerializer(room).data
            return APIResponse(status.HTTP_200_OK, data)
        except Exception as error:
            return APIResponse(status.HTTP_400_BAD_REQUEST, error.args[0])


class RoomDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)
            serializer = RoomSerializer(room).data
            return APIResponse(status.HTTP_200_OK, serializer)
        except Exception as error:
            return APIResponse(status.HTTP_404_NOT_FOUND, error.args[0])


class RoomUpdateAPIView(APIView):
    @extend_schema(
        request={
            "application/json": Room_parameters,
        }
    )
    def put(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)
            room = room.update(request.data)
            return APIResponse(status.HTTP_200_OK, RoomSerializer(room).data)
        except Exception as error:
            return APIResponse(status.HTTP_404_NOT_FOUND, error.args[0])


class RoomDeleteAPIView(APIView):
    def delete(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)
            room.delete()
            return APIResponse(status.HTTP_204_NO_CONTENT, "object deleted")
        except Exception as error:
            return APIResponse(status.HTTP_404_NOT_FOUND, error.args[0])


class RservationRoomAPIView(APIView):
    @extend_schema(
        request={
            "application/json": Roome_reservation_parameters,
        }
    )
    def post(self, request):
        try:
            valid, message = Roome_reservation_parameters.validate(request.data)
            if valid:
                reservation = Reservation.create(request.data)
                data = RoomeReservationSerilizer(reservation).data
                return APIResponse(status.HTTP_200_OK, data)
            else:
                raise serializers.ValidationError(message)
        except Exception as error:
            return APIResponse(status.HTTP_400_BAD_REQUEST, error.args[0])


class ReservedRooms(APIView):
    def get(self, request):
        try:
            rooms = Room.objects.filter(status="reserved")
            data = RoomSerializer(rooms, many=True).data
            return APIResponse(status.HTTP_200_OK, data)
        except Exception as error:
            return APIResponse(status.HTTP_404_NOT_FOUND, error.args[0])


class CheckReservedByDate(APIView):
    @extend_schema(
        request={
            "application/json": CheckReservedByDate_Parameters,
        }
    )
    def post(self, request):
        try:
            date = request.data["date"]
            available_rooms = []
            rooms = Room.objects.all()
            for room in rooms:
                is_available = room.check_room_by_date(date)
                if is_available:
                    available_rooms.append(room)
            data = RoomSerializer(available_rooms, many=True).data
            return APIResponse(status.HTTP_200_OK, data)
        except Exception as error:
            return APIResponse(status.HTTP_404_NOT_FOUND, error.args[0])


class CheckReservedByPeriod(APIView):
    @extend_schema(
        request={
            "application/json": CheckReservedByPeriod_Parameters,
        }
    )
    def post(self, request):
        try:
            start_date = request.data["start_date"]
            end_date = request.data["end_date"]
            available_rooms = []
            rooms = Room.objects.all()
            for room in rooms:
                is_available = room.check_room_by_period(start_date, end_date)
                if is_available:
                    available_rooms.append(room)
            data = RoomSerializer(available_rooms, many=True).data
            return APIResponse(status.HTTP_200_OK, data)
        except Exception as error:
            return APIResponse(status.HTTP_404_NOT_FOUND, error.args[0])
