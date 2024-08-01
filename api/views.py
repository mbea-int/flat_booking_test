from . import models, serializers
from .serializers import FlatSerializer, BookingSerializer
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework import filters


class FlatViewSet(viewsets.ModelViewSet):
    queryset = models.Flat.objects.all()
    serializer_class = FlatSerializer
    permission_classes = [AllowAny]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = models.Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['checkin']
    ordering = ['flat__id', 'checkin']
