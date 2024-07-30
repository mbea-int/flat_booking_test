from django.test import TestCase
from api import models


class TestModels(TestCase):
    def test_flat(self):
        flat = models.Flat.objects.create(name="flat-1")
        inserted_flat = models.Flat.objects.get(pk=flat.id)

        self.assertEqual("flat-1", inserted_flat.name)


