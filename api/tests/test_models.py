from django.test import TestCase

from api.models import CustomUser, Global


class TestCustomUserModel(TestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create(
            username='testuser',
            phone_number='1234567890',
            email='testemail@test.com'
        )
        self.user.set_password('testpassword123')
        self.user.save()

    def test_creating_a_user(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.phone_number, '1234567890')
        self.assertEqual(self.user.email, "testemail@test.com")

class TestGlobalModel(TestCase):
    def setUp(self) -> None:
        self.user = Global.objects.create(
            name='testuser',
            phone_number='1234567890',
            email='testemail@test.com'
        )
        self.user.save()

    def test_creating_a_user(self):
        self.assertEqual(self.user.name, "testuser")
        self.assertEqual(self.user.phone_number, '1234567890')
        self.assertEqual(self.user.email, "testemail@test.com")