"""
The HTTP async client for Eskiz.uz
"""
import logging
from typing import List, Optional, Dict, Any

import aiohttp
from aiohttp import ClientResponseError

from eskiz.enum import Network
from eskiz import request as eskiz_request
from eskiz import response as eskiz_response
from eskiz import exception as eskiz_exception


logger = logging.getLogger(__name__)


class AsyncClient:
    """
    The Eskiz HTTP async client
    """
    def __init__(
        self,
        email: str,
        password: str,
        network: str = Network.MAIN,
        from_: str = "4546",
        callback: str = "",
        token: Optional[str] = None,
    ):
        self.from_ = from_
        self.email = email
        self.password = password
        self.network = network
        self.callback = callback
        self.headers = {}
        self.token = token
        self._session = None

        # Set authorization header if token is provided
        if token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    async def _get_session(self) -> aiohttp.ClientSession:
        """
        Get or create an aiohttp session
        """
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _request(self, method: str, url: str, retry_count=0, **kwargs) -> Dict[str, Any]:
        """
        Make an HTTP request with automatic token refresh

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            retry_count: Current retry count (used internally)
            **kwargs: Additional request parameters
        """
        # Maximum number of retries for token refresh
        max_retries = 1

        session = await self._get_session()

        try:
            async with session.request(method, url, **kwargs) as response:
                response.raise_for_status()
                return await response.json()
        except ClientResponseError as exc:
            logger.error("HTTP error: %s", exc)

            # Handle token expiration with auto-refresh
            if exc.status == 401 and retry_count < max_retries:
                logger.info("Token expired, attempting to refresh")
                try:
                    # Try to refresh the token
                    await self._handle_token_expired()

                    # Update headers in kwargs if they exist
                    if 'headers' in kwargs:
                        kwargs['headers']["Authorization"] = f"Bearer {self.token}"

                    # Retry the request with the new token
                    return await self._request(method, url, retry_count + 1, **kwargs)
                except Exception as refresh_error:
                    logger.error("Token refresh failed: %s", refresh_error)
                    raise eskiz_exception.TokenExpired() from exc
            else:
                raise exc
        except Exception as exc:
            logger.error("Unexpected exception: %s", exc)
            raise exc

    async def initialize(self) -> None:
        """
        Initialize the client by logging in and setting the token

        If a token was provided in the constructor, it will be used.
        Otherwise, a new token will be obtained by logging in.
        """
        if self.token is None:
            logger.info("No token provided, logging in")
            response = await self.login()
            self.token = response.data.token
            self.headers["Authorization"] = f"Bearer {self.token}"

    async def login(self) -> eskiz_response.LoginResponse:
        """
        Authenticates with the Eskiz server
        """
        data = eskiz_request.LoginRequest(
            email=self.email,
            password=self.password,
        ).model_dump()

        url = f"{self.network}/api/auth/login"
        response = await self._request("POST", url, data=data)

        return eskiz_response.LoginResponse(**response)

    async def refresh_token(self) -> eskiz_response.RefreshTokenResponse:
        """
        Refreshes the given token

        Returns:
            RefreshTokenResponse object with the new token
        """
        url = f"{self.network}/api/auth/refresh"

        if self.token is None:
            await self.initialize()
            return None

        # Create a new session for token refresh to avoid recursion
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request("PATCH", url, headers=self.headers) as response:
                    response.raise_for_status()
                    response_data = await response.json()
                    token_response = eskiz_response.RefreshTokenResponse(**response_data)

                    # Update token and headers
                    self.token = token_response.data.token
                    self.headers["Authorization"] = f"Bearer {self.token}"

                    return token_response
            except Exception as e:
                logger.error("Token refresh failed: %s", e)
                raise

    async def _handle_token_expired(self) -> bool:
        """
        Handle token expiration by attempting to refresh the token

        Returns:
            bool: True if token was successfully refreshed, False otherwise
        """
        try:
            await self.refresh_token()
            return True
        except Exception as e:
            logger.warning("Token refresh failed, attempting to login again: %s", e)
            try:
                # Try to login again
                response = await self.login()
                self.token = response.data.token
                self.headers["Authorization"] = f"Bearer {self.token}"
                return True
            except Exception as login_error:
                logger.error("Login failed after token refresh failure: %s", login_error)
                return False

    async def _send_sms(self, phone_number: int, message: str) -> eskiz_response.SendSMSResponse:
        """
        Sends a new message to the given number

        Args:
            phone_number: The recipient phone number
            message: The message text
        """
        url = f"{self.network}/api/message/sms/send"

        files = eskiz_request.SendSMSRequest(
            phone_number=phone_number,
            message=message,
            from_=self.from_,
            callback_url=self.callback,
        ).to_file()

        # Convert files dict to FormData
        form_data = aiohttp.FormData()
        for key, value in files.items():
            form_data.add_field(key, value[1])

        response = await self._request("POST", url, data=form_data, headers=self.headers)

        return eskiz_response.SendSMSResponse(**response)

    async def send_sms(self, phone_number: int, message: str) -> eskiz_response.SendSMSResponse:
        """
        Sends a new message to the given number

        Args:
            phone_number: The recipient phone number
            message: The message text

        Returns:
            SendSMSResponse: Response from the API
        """
        if self.token is None:
            await self.initialize()

        try:
            return await self._send_sms(phone_number, message)
        except eskiz_exception.TokenExpired:
            await self.login()
            return await self._send_sms(phone_number, message)

    async def _send_batch_sms(
        self,
        messages: List[Dict[str, Any]],
        from_: str,
        dispatch_id: Optional[int] = None
    ) -> eskiz_response.SendBatchSMSResponse:
        """
        Sends batch SMS messages

        Args:
            messages: List of message dictionaries with user_sms_id, to, and text fields
            from_: Sender ID
            dispatch_id: Optional dispatch ID
        """
        url = f"{self.network}/api/message/sms/send-batch"

        # Convert the messages to JSON format
        data = {
            "messages": messages,
            "from": from_
        }

        if dispatch_id is not None:
            data["dispatch_id"] = dispatch_id

        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"

        response = await self._request("POST", url, json=data, headers=headers)

        return eskiz_response.SendBatchSMSResponse(**response)

    async def send_batch_sms(
        self,
        messages: List[Dict[str, Any]],
        from_: Optional[str] = None,
        dispatch_id: Optional[int] = None
    ) -> eskiz_response.SendBatchSMSResponse:
        """
        Sends multiple SMS messages in a single request

        Args:
            messages: List of message dictionaries with user_sms_id, to, and text fields
            from_: Sender ID (defaults to the client's from_ if not provided)
            dispatch_id: Optional dispatch ID for tracking

        Returns:
            SendBatchSMSResponse: Response from the API
        """
        if self.token is None:
            await self.initialize()

        sender = from_ if from_ is not None else self.from_

        try:
            return await self._send_batch_sms(messages, sender, dispatch_id)
        except eskiz_exception.TokenExpired:
            await self.login()
            return await self._send_batch_sms(messages, sender, dispatch_id)

    async def _send_global_sms(
        self,
        mobile_phone: str,
        message: str,
        country_code: str,
        callback_url: str = "",
        unicode: str = "0"
    ) -> eskiz_response.SendGlobalSMSResponse:
        """
        Sends SMS to international numbers

        Args:
            mobile_phone: Recipient phone number
            message: Message text
            country_code: Country code (e.g., "US")
            callback_url: Optional callback URL
            unicode: Unicode flag (0 or 1)
        """
        url = f"{self.network}/api/message/sms/send-global"

        files = eskiz_request.SendGlobalSMSRequest(
            mobile_phone=mobile_phone,
            message=message,
            country_code=country_code,
            callback_url=callback_url,
            unicode=unicode
        ).to_file()

        # Convert files dict to FormData
        form_data = aiohttp.FormData()
        for key, value in files.items():
            form_data.add_field(key, value[1])

        await self._request("POST", url, data=form_data, headers=self.headers)

        # Since the API returns 200 OK without a specific response body
        return eskiz_response.SendGlobalSMSResponse(success=True)

    async def send_global_sms(
        self,
        mobile_phone: str,
        message: str,
        country_code: str,
        callback_url: str = "",
        unicode: str = "0"
    ) -> eskiz_response.SendGlobalSMSResponse:
        """
        Sends SMS to international numbers

        Args:
            mobile_phone: Recipient phone number
            message: Message text
            country_code: Country code (e.g., "US")
            callback_url: Optional callback URL
            unicode: Unicode flag (0 or 1)

        Returns:
            SendGlobalSMSResponse: Response from the API
        """
        if self.token is None:
            await self.initialize()

        try:
            return await self._send_global_sms(
                mobile_phone, message, country_code, callback_url, unicode
            )
        except eskiz_exception.TokenExpired:
            await self.login()
            return await self._send_global_sms(
                mobile_phone, message, country_code, callback_url, unicode
            )

    async def _get_balance(self) -> eskiz_response.GetLimitResponse:
        """
        Fetches the SMS balance from Eskiz.uz
        """
        url = f"{self.network}/api/user/get-limit"
        response = await self._request("GET", url, headers=self.headers)
        return eskiz_response.GetLimitResponse(**response)

    async def get_balance(self) -> int:
        """
        Retrieves the current SMS balance

        Returns:
            int: Number of SMS credits remaining, or 0 if failed
        """
        if self.token is None:
            await self.initialize()

        try:
            response = await self._get_balance()
            if response.status == "success":
                return response.data.get("balance", 0)
            return 0
        except eskiz_exception.TokenExpired:
            await self.login()
            response = await self._get_balance()
            return response.data.get("balance", 0) if response.status == "success" else 0

    async def close(self) -> None:
        """
        Close the aiohttp session
        """
        if self._session is not None and not self._session.closed:
            await self._session.close()
            self._session = None

    async def __aenter__(self):
        """
        Async context manager entry
        """
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Async context manager exit
        """
        await self.close()
