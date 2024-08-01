from rest_framework import serializers
from .models import Flat, Booking
from datetime import date


def flatAvailable(validated_data):
    filter_params = dict(checkin__lte=validated_data['checkout'],
                         checkout__gte=validated_data['checkin'])
    is_occupied = Booking.objects.filter(**filter_params, flat=validated_data['flat']).exists()

    return False if is_occupied else True

def dates_valid(checkin_date, checkout_date):
    return False if not checkin_date \
                    or not checkout_date \
                    or checkin_date < date.today() \
                    or checkout_date < date.today() \
                    or checkout_date < checkin_date \
        else True


class FlatSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=255)

    class Meta:
        model = Flat
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    flat = serializers.PrimaryKeyRelatedField(queryset=Flat.objects.prefetch_related('bookings'), write_only=True,  many=False)
    flat_name = serializers.CharField(source='flat.name', read_only=True)
    previous_booking_id = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['flat', 'flat_name', 'id', 'checkin', 'checkout', 'previous_booking_id']

    def get_previous_booking_id(self, obj):
        prev_bookings = Booking.objects.filter(flat=obj.flat, checkin__lt=obj.checkin).order_by("-checkin")
        return prev_bookings[0].id if prev_bookings else '-'

    def create(self, validated_data):
        # flat = Flat.objects.get(name=validated_data["flat"])
        checkin = validated_data.get("checkin")
        checkout = validated_data.get("checkout")
        if not dates_valid(checkin, checkout):
            raise serializers.ValidationError({
                "detail": f"The selected date range (checkin: {checkin} checkout: {checkout}) is invalid."
            })
        if flatAvailable(validated_data):
            return Booking.objects.create(**validated_data)

        else:
            raise serializers.ValidationError({
                "detail": "Flat is not available for these dates."
            })

    def update(self, instance, validated_data):
        checkin = validated_data.get("checkin", instance.checkin)
        checkout = validated_data.get("checkout", instance.checkout)
        if not dates_valid(checkin, checkout):
            raise serializers.ValidationError({
                "detail": "The selected date range is invalid."
            })
        if flatAvailable(validated_data):
            instance.checkin = checkin
            instance.checkout = checkout
            #Omitting the flat because we don't want it to be updated
            # instance.flat = validated_data.get('flat', instance.flat)
            instance.save()
        else:
            raise serializers.ValidationError({
                "detail": "Flat is not available for these dates."
            })
        return instance