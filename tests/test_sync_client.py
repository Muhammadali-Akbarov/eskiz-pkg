"""
Tests for the synchronous client
"""
import unittest
from unittest.mock import patch, MagicMock

from eskiz.client.sync import ClientSync
from eskiz.response.login import LoginResponse
from eskiz.response.send import SendSMSResponse


class TestClientSync(unittest.TestCase):
    """
    Test cases for the synchronous client
    """
    def setUp(self):
        """
        Set up test environment
        """
        self.client = ClientSync(
            email="test@eskiz.uz",
            password="password",
        )
        
        # Mock the token
        self.client.token = "test_token"
        self.client.headers = {"Authorization": f"Bearer {self.client.token}"}

    @patch('eskiz.client.http.HttpClient.request')
    def test_login(self, mock_request):
        """
        Test login functionality
        """
        # Mock response
        mock_response = {
            "message": "token created",
            "data": {
                "token": "test_token"
            },
            "token_type": "bearer"
        }
        mock_request.return_value = mock_response
        
        # Call login
        response = self.client.login()
        
        # Assertions
        self.assertIsInstance(response, LoginResponse)
        self.assertEqual(response.data.token, "test_token")
        self.assertEqual(self.client.token, "test_token")
        self.assertEqual(self.client.headers["Authorization"], "Bearer test_token")
        
        # Verify request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertIn("/api/auth/login", args[1])

    @patch('eskiz.client.http.HttpClient.request')
    def test_send_sms(self, mock_request):
        """
        Test send SMS functionality
        """
        # Mock response
        mock_response = {
            "id": "123",
            "status": "waiting",
            "message": "SMS sent"
        }
        mock_request.return_value = mock_response
        
        # Call send_sms
        response = self.client.send_sms(
            phone_number=998888351717,
            message="Test message"
        )
        
        # Assertions
        self.assertIsInstance(response, SendSMSResponse)
        self.assertEqual(response.id, "123")
        self.assertEqual(response.status, "waiting")
        
        # Verify request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertIn("/api/message/sms/send", args[1])
        self.assertIn("files", kwargs)
        
        # Check files content
        files = kwargs["files"]
        self.assertEqual(files["mobile_phone"][1], "998888351717")
        self.assertEqual(files["message"][1], "Test message")


if __name__ == "__main__":
    unittest.main()
