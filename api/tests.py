from api import models
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestModels(APITestCase):

    def test_flat(self):
        """
        Testing the creation of flats
        :return:
        """
        flat = models.Flat.objects.create(name="flat-1")
        inserted_flat = models.Flat.objects.get(pk=flat.id)

        self.assertEqual("flat-1", inserted_flat.name)

    def test_booking(self):
        """
        Testing the creation of bookings
        :return:
        """
        flat = models.Flat.objects.create(name="flat-1")
        models.Booking.objects.create(flat=flat, checkin="2024-08-04", checkout="2024-08-05")

        inserted_booking = models.Booking.objects.get(flat=flat)

        self.assertEqual(models.Booking.objects.count(), 1)
        self.assertEqual(models.Booking.objects.get().flat.name, 'flat-1')
        self.assertEqual("2024-08-04", inserted_booking.checkin.strftime("%Y-%m-%d"))
        self.assertEqual("2024-08-05", inserted_booking.checkout.strftime("%Y-%m-%d"))


class BookingViewsTestCase(APITestCase):
    def setUp(self) -> None:
        """
        Initial data to test the listing and ordering of bookings.
        We have created 2 flats and 5 initial booking data.
        :return:
        """
        self.url = reverse("api:booking-list")
        self.flat_1 = models.Flat.objects.create(name="flat-1")
        self.flat_2 = models.Flat.objects.create(name="flat-2")
        self.booking_1 = models.Booking.objects.create(
            flat=self.flat_1,
            checkin="2022-01-01",
            checkout="2022-01-13"
        )
        self.booking_2 = models.Booking.objects.create(
            flat=self.flat_1,
            checkin="2022-01-20",
            checkout="2022-02-10"
        )
        self.booking_3 = models.Booking.objects.create(
            flat=self.flat_1,
            checkin="2022-02-20",
            checkout="2022-03-10"
        )
        self.booking_4 = models.Booking.objects.create(
            flat=self.flat_2,
            checkin="2022-01-02",
            checkout="2022-01-20"
        )
        self.booking_5 = models.Booking.objects.create(
            flat=self.flat_2,
            checkin="2022-01-20",
            checkout="2022-02-11"
        )

    def test_get_bookings(self):
        """
        Testing if we get the bookings by their default order (flat id and booking checking)
        :return:
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

        self.assertEqual(response.data[0], {'flat_name': 'flat-1',
                                            'id': 1,
                                            'checkin': '2022-01-01',
                                            'checkout': '2022-01-13',
                                            'previous_booking_id': '-'})
        self.assertEqual(response.data[1], {'flat_name': 'flat-1',
                                            'id': 2,
                                            'checkin': '2022-01-20',
                                            'checkout': '2022-02-10',
                                            'previous_booking_id': 1})
        self.assertEqual(response.data[2], {'flat_name': 'flat-1',
                                            'id': 3,
                                            'checkin': '2022-02-20',
                                            'checkout': '2022-03-10',
                                            'previous_booking_id': 2})
        self.assertEqual(response.data[3], {'flat_name': 'flat-2',
                                            'id': 4,
                                            'checkin': '2022-01-02',
                                            'checkout': '2022-01-20',
                                            'previous_booking_id': '-'})
        self.assertEqual(response.data[4], {'flat_name': 'flat-2',
                                            'id': 5,
                                            'checkin': '2022-01-20',
                                            'checkout': '2022-02-11',
                                            'previous_booking_id': 4})

    def test_booking_order_by_checkin_desc(self):
        """
        Testing if we can order the bookings by the checkin field in the descending order
        :return:
        """
        params = {"ordering": "-checkin"}
        response = self.client.get(self.url, data=params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

        self.assertEqual(response.data[0], {'flat_name': 'flat-1',
                                            'id': 3,
                                            'checkin': '2022-02-20',
                                            'checkout': '2022-03-10',
                                            'previous_booking_id': 2})

    def test_booking_order_by_checkin_asc(self):
        """
        Testing if we can order the bookings by the checkin field in the ascending order
        :return:
        """
        params = {"ordering": "checkin"}
        response = self.client.get(self.url, data=params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

        self.assertEqual(response.data[0], {'flat_name': 'flat-1',
                                            'id': 1,
                                            'checkin': '2022-01-01',
                                            'checkout': '2022-01-13',
                                            'previous_booking_id': '-'})

    def test_post_booking(self):
        """
        Testing if we can create a new booking via our API
        :return:
        """
        sample_booking = {
            "flat": self.flat_1.id,
            "checkin": "2024-08-04",
            "checkout": "2024-08-07"
        }
        response = self.client.post(self.url, sample_booking, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["checkin"], sample_booking["checkin"])
        self.assertEqual(response.data["checkout"], sample_booking["checkout"])
        self.assertEqual(response.data["flat_name"], self.flat_1.name)

    def test_booking_get_one_record(self):
        self.details_url = reverse("api:booking-detail", args=[self.flat_1.id])

        response = self.client.get(self.details_url, format='json')

        the_booking = models.Booking.objects.get(id=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(the_booking.checkin.strftime("%Y-%m-%d"), response.data["checkin"])
        self.assertEqual(the_booking.checkout.strftime("%Y-%m-%d"), response.data["checkout"])

    def test_booking_update(self):
        self.details_url = reverse("api:booking-detail", args=[self.flat_1.id])
        sample_booking = {
            "flat": self.flat_1.id,
            "checkin": "2024-08-04",
            "checkout": "2024-08-07"
        }
        response = self.client.put(self.details_url, sample_booking, format='json')

        updated_booking = models.Booking.objects.get(id=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_booking.checkin.strftime("%Y-%m-%d"), sample_booking["checkin"])
        self.assertEqual(updated_booking.checkout.strftime("%Y-%m-%d"), sample_booking["checkout"])
        self.assertEqual(updated_booking.flat.name, self.flat_1.name)

    def test_booking_delete(self):
        self.details_url = reverse("api:booking-detail", args=[self.flat_1.id])

        response = self.client.delete(self.details_url, format='json')

        bookings = models.Booking.objects.all()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(bookings), 4)


class FlatViewsTestCase(APITestCase):
    def test_flat_create(self):
        payload = {
            "name": "flat-1"
        }
        res = self.client.post(reverse("api:flat-list"), payload, format="json")

        self.assertEqual(201, res.status_code)

        json_res = res.json()

        self.assertEqual(payload["name"], json_res["name"])
        self.assertIsInstance(json_res["id"], int)

    def test_flat_list(self):
        res = self.client.get(reverse("api:flat-list"), format="json")

        self.assertEqual(status.HTTP_200_OK, res.status_code)

        json_res = res.json()

        self.assertIsInstance(json_res, list)

        flats = models.Flat.objects.all()
        self.assertEqual(len(flats), len(json_res))

    def test_flat_create_required_field_missing(self):
        payload = {}
        res = self.client.post(reverse("api:flat-list"), payload, format="json")
        self.assertEqual(400, res.status_code)

    def test_flat_retrieve(self):
        flat = models.Flat.objects.create(name="flat-1")

        res = self.client.get(reverse("api:flat-detail", args=[flat.id]), format="json")

        self.assertEqual(200, res.status_code)

        json_res = res.json()

        self.assertEqual(flat.id, json_res["id"])
        self.assertEqual(flat.name, json_res["name"])

    def test_flat_delete(self):
        flat = models.Flat.objects.create(name="flat-1")

        res = self.client.delete(reverse("api:flat-detail", args=[flat.id]), format="json")

        self.assertEqual(204, res.status_code)

        self.assertFalse(models.Flat.objects.filter(pk=flat.id).exists())
