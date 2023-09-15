from django.urls import path
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from .views import (
    RoomCreateAPIView,
    RoomDetailAPIView,
    RoomUpdateAPIView,
    RoomDeleteAPIView,
    RservationRoomAPIView,
    ReservedRooms,
    CheckReservedByDate,
    CheckReservedByPeriod,
)


schema_view = get_schema_view(
    openapi.Info(
        title="Room Booking API",
        default_version="v1",
        description="API for managing room bookings",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Example License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("create", RoomCreateAPIView.as_view(), name="add-room"),
    path("detail/<int:pk>/", RoomDetailAPIView.as_view(), name="room-detail"),
    path("update/<int:pk>/", RoomUpdateAPIView.as_view(), name="room-update"),
    path("delete/<int:pk>/", RoomDeleteAPIView.as_view(), name="room-delete"),
    path("reservaition/", RservationRoomAPIView.as_view(), name="room-reservaition"),
    path("reserved/", ReservedRooms.as_view(), name="room-reserved"),
    path(
        "check_rooms_by_date/",
        CheckReservedByDate.as_view(),
        name="room-check_rooms_by_date",
    ),
    path(
        "check_rooms_by_period/",
        CheckReservedByPeriod.as_view(),
        name="room-check_rooms_by_period",
    ),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
