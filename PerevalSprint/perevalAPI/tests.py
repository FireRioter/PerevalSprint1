from django.test import TestCase
from django.urls import reverse
from .models import Pereval, Coords, Levels, Users


class PerevalTestCase(TestCase):
    def setUp(self):
        self.pereval = Pereval.objects.create(
            title="Test Pereval",
            beauty_title="Test Pereval",
            coords=Coords.objects.create(
                latitude=228,
                longitude=228,
                height=228,
            ),
            level=Levels.objects.create(
                summer="1A", winter="1B", autumn="1C", spring="1D"
            ),
            user=Users.objects.create(
                email="test@email.com",
                fam="Test",
                name="Test",
                otc="Test",
                phone="79161234567",
            ),
        )

    def test_pereval_model(self):
        self.assertEqual((self.pereval.id), self.pereval.id)

    def test_pereval_list_view(self):
        response = self.client.get(reverse("perevals-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.pereval.title.encode(), response.content)

    def test_pereval_detail_view(self):
        response = self.client.get(reverse("perevals-detail", args=[self.pereval.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.pereval.title.encode(), response.content)

    def test_list_perevals_by_email(self):
        response = self.client.get(
            reverse("emailes-list"), {"user__email": self.pereval.user.email}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Pereval")
