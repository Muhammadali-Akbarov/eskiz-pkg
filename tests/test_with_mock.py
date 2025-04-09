"""
Test the Eskiz.uz client with a mock server
"""
import os
import sys
import unittest
import threading
import time
from unittest.mock import patch

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.mock_server import run_mock_server
from eskiz.client.sync import ClientSync
from eskiz.enum import Network


class TestWithMockServer(unittest.TestCase):
    """
    Test the Eskiz.uz client with a mock server
    """
    @classmethod
    def setUpClass(cls):
        """
        Start the mock server
        """
        cls.mock_server_port = 8765
        cls.mock_server_thread = threading.Thread(
            target=run_mock_server,
            args=(cls.mock_server_port,),
            daemon=True
        )
        cls.mock_server_thread.start()
        time.sleep(1)  # Give the server time to start

    def setUp(self):
        """
        Set up the test client
        """
        self.client = ClientSync(
            email="test@example.com",
            password="password",
            network=f"http://localhost:{self.mock_server_port}"
        )

    def test_login(self):
        """
        Test login functionality
        """
        response = self.client.login()
        self.assertEqual(response.data.token, "mock_token_12345")
        self.assertEqual(self.client.token, "mock_token_12345")

    def test_send_sms(self):
        """
        Test send SMS functionality
        """
        response = self.client.send_sms(
            phone_number=998901234567,
            message="Test message"
        )
        self.assertEqual(response.id, "mock-message-id-12345")
        self.assertEqual(response.status, "waiting")

    def test_send_batch_sms(self):
        """
        Test send batch SMS functionality
        """
        messages = [
            {"user_sms_id": "msg1", "to": 998901234567, "text": "First message"},
            {"user_sms_id": "msg2", "to": 998901234568, "text": "Second message"}
        ]
        response = self.client.send_batch_sms(messages=messages)
        self.assertEqual(response.id, "mock-message-id-12345")
        self.assertEqual(response.status, "waiting")

    def test_get_balance(self):
        """
        Test get balance functionality
        """
        balance = self.client.get_balance()
        self.assertEqual(balance, 1000)

    def test_get_message_status(self):
        """
        Test get message status functionality
        """
        response = self.client.get_message_status("mock-message-id-12345")
        self.assertEqual(response.data.status, "delivered")
        self.assertEqual(response.data.to, "998901234567")

    def test_get_templates(self):
        """
        Test get templates functionality
        """
        response = self.client.get_templates()
        self.assertEqual(len(response.result), 2)
        self.assertEqual(response.result[0].id, 1)
        self.assertEqual(response.result[0].template, "Hello, {name}! Welcome to our service.")

    def test_get_user_messages(self):
        """
        Test get user messages functionality
        """
        response = self.client.get_user_messages(
            start_date="2023-01-01 00:00",
            end_date="2023-12-31 23:59"
        )
        self.assertEqual(response.data.total, 2)
        self.assertEqual(response.data.result[0].to, "998901234567")
        self.assertEqual(response.data.result[1].to, "998901234568")


if __name__ == "__main__":
    unittest.main()
