# tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Account, Destination
import uuid

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.account = Account.objects.create(
            email="test@example.com",
            name="Test Account",
            app_secret_token=str(uuid.uuid4())
        )
        self.destination = Destination.objects.create(
            account=self.account,
            url="http://example.com",
            http_method="POST",
            headers={"Content-Type": "application/json"}
        )

    def test_create_account(self):
        response = self.client.post("/accounts/", {"email": "new@example.com", "name": "New Account"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_accounts(self):
        response = self.client.get("/accounts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_incoming_data_without_token(self):
        response = self.client.post("/server/incoming_data/", {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_incoming_data_with_invalid_token(self):
        response = self.client.post("/server/incoming_data/", {}, HTTP_CL_X_TOKEN="invalid_token")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
