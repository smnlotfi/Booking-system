from django.db import models
from datetime import timedelta, datetime

# Create your models here.


class Room(models.Model):
    status_choice = (("available", "available"), ("reserved", "reserved"))
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to="room_pictures/")
    detail = models.TextField()
    status = models.CharField(
        max_length=200, choices=status_choice, default="available"
    )
    reserved_dates = models.ManyToManyField(
        "Reservation", related_name="reserverde_date"
    )
    price = models.IntegerField(null=True)

    @classmethod
    def create(cls, data):
        return cls.objects.create(**data)

    def update(self, data):
        for field, value in data.items():
            setattr(self, field, value)
        self.save()
        return self

    def get_reserved_dates(self):
        dates = []
        queryset = Reservation.objects.filter(room=self)
        for query in queryset:
            date = query.start_date
            while date <= query.end_date:
                dates.append(date)
                date = date + timedelta(days=1)
        return dates

    def check_room_by_date(self, date):
        date = datetime.strptime(date, "%Y-%m-%d").date()
        res = True
        reserved_dates = self.get_reserved_dates()
        if date in reserved_dates:
            res = False
        return res

    def check_room_by_period(self, start_date, end_date):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        reserve_dates = self.get_reserved_dates()
        start_date = start_date
        result = True
        while start_date <= end_date:
            if start_date in reserve_dates:
                result = False
                break
            else:
                start_date = start_date + timedelta(days=1)

        return result


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    paid = models.BooleanField(default=False)

    @classmethod
    def create(cls, data):
        room = Room.objects.get(id=data["room_id"])
        start_date = data["start_date"]
        end_date = data["end_date"]
        reservation = Reservation.objects.create(
            room=room, start_date=start_date, end_date=end_date, paid=True
        )
        room.status = "reserved"
        room.save()
        return reservation
