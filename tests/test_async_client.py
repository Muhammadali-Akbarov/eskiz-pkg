"""
Tests for the asynchronous client
"""
import unittest
from unittest.mock import patch, MagicMock

import pytest

from eskiz.client.async_client import AsyncClient
from eskiz.response.login import LoginResponse
from eskiz.response.send import SendSMSResponse


class TestAsyncClient(unittest.IsolatedAsyncioTestCase):
    """
    Test cases for the asynchronous client
    """
    async def asyncSetUp(self):
        """
        Set up test environment
        """
        self.client = AsyncClient(
            email="test@eskiz.uz",
            password="password",
        )
        
        # Mock the token
        self.client.token = "test_token"
        self.client.headers = {"Authorization": f"Bearer {self.client.token}"}
        
        # Mock session
        self.client._session = MagicMock()
        self.client._get_session = MagicMock(return_value=self.client._session)

    @patch('aiohttp.ClientSession.request')
    async def test_login(self, mock_request):
        """
        Test login functionality
        """
        # Mock response
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json = MagicMock(return_value={
            "message": "token created",
            "data": {
                "token": "test_token"
            },
            "token_type": "bearer"
        })
        mock_response.__aenter__ = MagicMock(return_value=mock_response)
        mock_response.__aexit__ = MagicMock(return_value=None)
        mock_request.return_value = mock_response
        
        # Call login
        response = await self.client.login()
        
        # Assertions
        self.assertIsInstance(response, LoginResponse)
        self.assertEqual(response.data.token, "test_token")
        
        # Verify request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertIn("/api/auth/login", args[1])

    @patch('aiohttp.ClientSession.request')
    async def test_send_sms(self, mock_request):
        """
        Test send SMS functionality
        """
        # Mock response
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json = MagicMock(return_value={
            "id": "123",
            "status": "waiting",
            "message": "SMS sent"
        })
        mock_response.__aenter__ = MagicMock(return_value=mock_response)
        mock_response.__aexit__ = MagicMock(return_value=None)
        mock_request.return_value = mock_response
        
        # Call send_sms
        response = await self.client.send_sms(
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
        self.assertIn("data", kwargs)


if __name__ == "__main__":
    unittest.main()
