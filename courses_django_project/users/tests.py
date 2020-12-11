from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"username": "username", "password": "password"}
        response = self.client.post("/api/v1/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
