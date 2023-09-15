# rooms/serializers.py
from rest_framework import serializers
from .models import Room, Reservation
from rest_framework.response import Response
from datetime import timedelta


class RoomeReservationDateSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["start_date", "end_date"]


class RoomSerializer(serializers.ModelSerializer):
    reserved_dates = serializers.SerializerMethodField()

    def get_reserved_dates(self, obj):
        dates = []
        queryset = Reservation.objects.filter(room=obj)
        for query in queryset:
            date = query.start_date
            while date <= query.end_date:
                dates.append(date)
                date = date + timedelta(days=1)
        return dates

    class Meta:
        model = Room
        fields = "__all__"


class RoomeReservationSerilizer(serializers.ModelSerializer):
    room = RoomSerializer()

    class Meta:
        model = Reservation
        fields = ["start_date", "end_date", "room"]


def APIResponse(status, data=None, redirect_to=None):
    response = {"status": status}
    response["data"] = data if data else None
    if redirect_to:
        response["redirect_to"] = redirect_to
    return Response(response)
