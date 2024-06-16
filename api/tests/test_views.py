from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import CustomUser, Global, Spam


class CustomUserRegistrationTest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('register')
 
    def test_user_registration(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'phone_number': '1234567890',
            'email': 'testuser@test.com'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'testuser')
    
    def test_user_registration_without_mandatory_field(self):
        data = {
            'phone_number': '1234567890',
            'password': 'testpassword123',
            'email': 'testuser@test.com'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(response.content, {'Message': 'Error while registering the user', 'Error': {'username': ['This field is required.']}})
 
    
    def test_user_registration_with_less_phone_number(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'phone_number': '34567890',
            'email': 'testuser@test.com'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(response.content, {'Message': 'Error while registering the user', 'Error': {'phone_number': ["Phone number must be exactly 10 digits."]}})

    def test_user_registration_with_large_phone_number(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'phone_number': '123456789011',
            'email': 'testuser@test.com'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(response.content, {'Message': 'Error while registering the user', 'Error': {'phone_number': ['Ensure this field has no more than 10 characters.']}})   

class CustomUserLoginTest(APITestCase):
    def setUp(self):
        self.url = reverse('login')
        self.user = CustomUser.objects.create(
            username='testuser',
            phone_number='9876543210'
        )
        self.user.set_password('testpassword123')
        self.user.save()

    def test_user_login(self):
        data = {
            'phone_number': '9876543210',
            'password': 'testpassword123',
            'username': 'testuser',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_invalid_credentials(self):
        data = {
            'phone_number': '9876543210',
            'password': 'wrongpassword',
            'username': 'testuser'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_login_invalid_credentials(self):
        data = {
            'phone_number': '9876543210',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class SpamTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser1', phone_number='9876543210', password='testpassword123')
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.global_db = Global.objects.create(name='user1', phone_number='8967543210')
        self.url = reverse('spam') 

    def test_mark_as_spam(self):
        data = {
            'phone_number': '8967543210',
            'reason': 'Telemarketing'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, {'Message': 'Marked as spam'})   
        self.global_db.refresh_from_db()
        self.assertTrue(self.global_db.spam)
        self.assertEqual(Spam.objects.count(), 1)
    
    def test_mark_as_spam_for_mandatory_fields(self):
        data = {
            'reason': 'Telemarketing'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(response.content, {'Message': 'Error while marking the number as spam', 'Error': {'phone_number': ['This field is required.']}})   

    def test_mark_as_spam_using_phone_number_not_in_global_db(self):
        data = {
            'phone_number': '8967543211',
            'reason': 'Telemarketing'
        }
        self.assertEqual(Spam.objects.count(), 0)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, {'Message': 'Added to global db as spam'})   
        self.global_db.refresh_from_db()
        self.assertEqual(Spam.objects.count(), 1)
        self.assertEqual(Global.objects.count(), 2)

class GlobalTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser1', phone_number='9876543210', password='testpassword123')
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.spam = Spam.objects.create(phone_number='8967543210', reason='Telemarketing', reported_by=self.user)
        Global.objects.create(name='user1', phone_number='8967543210', spam=self.spam)
        Global.objects.create(name='testuser2', phone_number='8967543211')
        Global.objects.create(name='user', phone_number='8967543212', email="testemail@email.com")
        Global.objects.create(name='user4', phone_number='8967543213')
        self.url = reverse('global')
    
    def test_get_single_person_using_name(self):
        data = {
            'query': 'user1',
            'type': 'name'
        }
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, {'query_data': [{'name': 'user1', 'phone_number': '8967543210', 'spam': 4, 'email': None}]})
    
    def test_get_multiple_person_using_name(self):
        data = {
            'query': 'user',
            'type': 'name'
        }
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, {'query_data': [{'name': 'user', 'phone_number': '8967543212', 'spam': None, 'email': 'testemail@email.com'}, 
                                                               {'name': 'user1', 'phone_number': '8967543210', 'spam': 1, 'email': None},
                                                               {'name': 'user4', 'phone_number': '8967543213', 'spam': None, 'email': None}, 
                                                               {'name': 'testuser2', 'phone_number': '8967543211', 'spam': None, 'email': None}]})
    
    def test_get_single_person_using_phone_number(self):
        data = {
            'query': '8967543212',
            'type': 'phone_number'
        }
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, {'query_data': [{'name': 'user', 'phone_number': '8967543212', 'spam': None, 'email': 'testemail@email.com'}]})
    
    def test_get_multiple_person_using_phone_number(self):
        data = {
            'query': '8967',
            'type': 'phone_number'
        }
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, {'query_data': [{'name': 'testuser2', 'phone_number': '8967543211', 'spam': None, 'email': None}, 
                                                               {'name': 'user', 'phone_number': '8967543212', 'spam': None, 'email': 'testemail@email.com'}, 
                                                               {'name': 'user1', 'phone_number': '8967543210', 'spam': 2, 'email': None},
                                                               {'name': 'user4', 'phone_number': '8967543213', 'spam': None, 'email': None}, ]})
    
    def test_get_person_for_invaild_type(self):
        data = {
            'query': '8967',
            'type': 'email'
        }
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(response.content, {'Error': 'Invalid query type'})

    