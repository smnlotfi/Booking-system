from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers
from .models import Room, Reservation
from rest_framework.response import Response
from datetime import datetime, timedelta


class Room_parameters(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["title", "picture", "detail", "price"]


class Room_id__for_Roome_reservation_parameters(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id"]


class Roome_reservation_parameters(serializers.ModelSerializer):
    room_id = serializers.IntegerField()

    @classmethod
    def validate(cls, data):
        room_id = data["room_id"]
        start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
        if start_date < end_date:
            if Roome_reservation_parameters().validate_for_reserve(
                start_date, end_date, room_id
            ):
                return True, None
            else:
                return False, "this date reserved"
        else:
            False, "Start date must be before end date"

    @classmethod
    def validate_for_reserve(cls, start_date, end_date, room_id):
        reserve_dates = Roome_reservation_parameters().get_reserved_dates(room_id)
        start_date = start_date
        result = True
        while start_date <= end_date:
            if start_date in reserve_dates:
                result = False
                break
            else:
                start_date = start_date + timedelta(days=1)

        return result

    @classmethod
    def get_reserved_dates(cls, room_id):
        dates = []
        queryset = Reservation.objects.filter(room=Room.objects.get(id=room_id))
        for query in queryset:
            date = query.start_date
            while date <= query.end_date:
                dates.append(date)
                date = date + timedelta(days=1)
        return dates

    class Meta:
        model = Reservation
        fields = ["start_date", "end_date", "room_id"]


class CheckReservedByDate_Parameters(serializers.ModelSerializer):
    date = serializers.DateField()
    room_id = serializers.IntegerField()

    class Meta:
        model = Room
        fields = ["room_id", "date"]


class CheckReservedByPeriod_Parameters(serializers.ModelSerializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    room_id = serializers.IntegerField()

    class Meta:
        model = Room
        fields = ["room_id", "start_date", "end_date"]
