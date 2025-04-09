"""
The HTTP synchronous client for Eskiz.uz
"""
import logging
from typing import List, Optional, Dict, Any

from eskiz.enum import Network
from eskiz.client.http import HttpClient
from eskiz import request as eskiz_request
from eskiz import response as eskiz_response
from eskiz import exception as eskiz_exception

logger = logging.getLogger(__name__)


class ClientSync:
    """
    The Eskiz HTTP sync client
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

        # Initialize HTTP client with token refresh callback
        self.client = HttpClient(token_refresh_callback=self._handle_token_expired)

        # Login if no token provided
        if not token:
            response = self.login()
            self.token = response.data.token
            self.headers["Authorization"] = f"Bearer {self.token}"
        else:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def login(self, timeout=60) -> eskiz_response.LoginResponse:
        """
        Authenticates with the Eskiz server
        """
        method = "POST"
        data = eskiz_request.LoginRequest(
            email=self.email,
            password=self.password,
        ).model_dump()

        url = f"{self.network}/api/auth/login"

        response = self.client.request(
            url=url,
            data=data,
            method=method,
            timeout=timeout
        )
        return eskiz_response.LoginResponse(**response)

    def refresh_token(self, timeout=60) -> eskiz_response.RefreshTokenResponse:
        """
        Refreshes the given token

        Args:
            timeout: Request timeout in seconds

        Returns:
            RefreshTokenResponse object with the new token
        """
        url = f"{self.network}/api/auth/refresh"

        # Use a temporary client without token refresh callback to avoid infinite recursion
        temp_client = HttpClient()
        headers = self.headers

        try:
            response = temp_client.request("PATCH", url, headers=headers, timeout=timeout)
            refresh_response = eskiz_response.RefreshTokenResponse(**response)

            # Update token and headers
            self.token = refresh_response.data.token
            self.headers["Authorization"] = f"Bearer {self.token}"

            return refresh_response
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            raise

    def _handle_token_expired(self) -> bool:
        """
        Handle token expiration by attempting to refresh the token

        Returns:
            bool: True if token was successfully refreshed, False otherwise
        """
        try:
            logger.info("Token expired, attempting to refresh")
            self.refresh_token()
            return True
        except Exception as e:
            logger.warning(f"Token refresh failed, attempting to login again: {e}")
            try:
                # Try to login again
                response = self.login()
                self.token = response.data.token
                self.headers["Authorization"] = f"Bearer {self.token}"
                return True
            except Exception as login_error:
                logger.error(f"Login failed after token refresh failure: {login_error}")
                return False

    def _user(self, timeout=60) -> eskiz_response.UserResponse:
        """
        Retrieves user information
        """
        url = f"{self.network}/api/auth/user"

        headers = self.headers
        response = self.client.request("GET", url, headers=headers, timeout=timeout)

        return eskiz_response.UserResponse(**response)

    def _send_sms(self, phone_number: int, message: str, timeout=60) -> eskiz_response.SendSMSResponse:
        """
        Sends a new message to the given number
        Args:
            phone_number (str): The recipient phone number
            message (str): The message text
            timeout (int, optional): The request timeout. Defaults to 60.
        """
        url = f"{self.network}/api/message/sms/send"

        files = eskiz_request.SendSMSRequest(
            phone_number=phone_number,
            message=message,
            from_=self.from_,
            callback_url=self.callback,
        ).to_file()

        headers = self.headers
        response = self.client.request("POST", url, files=files, timeout=timeout, headers=headers)

        return eskiz_response.SendSMSResponse(**response)

    def user(self, timeout=60) -> eskiz_response.UserResponse:
        """
        Retrieves user information
        """
        try:
            return self._user(timeout)
        except eskiz_exception.TokenExpired:
            self.login(timeout)
            return self._user(timeout)

    def send_sms(self, phone_number: int, message: str, timeout=60) -> eskiz_response.SendSMSResponse:
        """
        Sends a new message to the given number
        Args:
            phone_number (str): The recipient phone number
            message (str): The message text
            timeout (int, optional): The request timeout. Defaults to 60.
        """
        try:
            return self._send_sms(phone_number, message, timeout)
        except eskiz_exception.TokenExpired:
            self.login(timeout)
            return self._send_sms(phone_number, message, timeout)

    def _get_balance(self, timeout=60) -> eskiz_response.GetLimitResponse:
        """
        Fetches the SMS balance from Eskiz.uz.
        """
        url = f"{self.network}/api/user/get-limit"
        headers = self.headers
        response = self.client.request("GET", url, headers=headers, timeout=timeout)
        return eskiz_response.GetLimitResponse(**response)

    def get_balance(self, timeout=60) -> int:
        """
        Retrieves the current SMS balance.

        Returns:
            int: Number of SMS credits remaining, or 0 if failed.
        """
        try:
            response = self._get_balance(timeout)
            if response.status == "success":
                return response.data.get("balance", 0)
            return 0
        except eskiz_exception.TokenExpired:
            self.login(timeout)
            response = self._get_balance(timeout)
            return response.data.get("balance", 0) if response.status == "success" else 0

    def _send_batch_sms(self, messages: List[Dict[str, Any]], from_: str, dispatch_id: Optional[int] = None,
                        timeout=60) -> eskiz_response.SendBatchSMSResponse:
        """
        Sends batch SMS messages

        Args:
            messages: List of message dictionaries with user_sms_id, to, and text fields
            from_: Sender ID
            dispatch_id: Optional dispatch ID
            timeout: Request timeout in seconds
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

        response = self.client.request(
            "POST",
            url,
            json=data,
            headers=headers,
            timeout=timeout
        )

        return eskiz_response.SendBatchSMSResponse(**response)

    def send_batch_sms(self, messages: List[Dict[str, Any]], from_: Optional[str] = None,
                      dispatch_id: Optional[int] = None, timeout=60) -> eskiz_response.SendBatchSMSResponse:
        """
        Sends multiple SMS messages in a single request

        Args:
            messages: List of message dictionaries with user_sms_id, to, and text fields
            from_: Sender ID (defaults to the client's from_ if not provided)
            dispatch_id: Optional dispatch ID for tracking
            timeout: Request timeout in seconds

        Returns:
            SendBatchSMSResponse: Response from the API
        """
        sender = from_ if from_ is not None else self.from_

        try:
            return self._send_batch_sms(messages, sender, dispatch_id, timeout)
        except eskiz_exception.TokenExpired:
            self.login(timeout)
            return self._send_batch_sms(messages, sender, dispatch_id, timeout)

    def _send_global_sms(self, mobile_phone: str, message: str, country_code: str,
                        callback_url: str = "", unicode: str = "0", timeout=60) -> eskiz_response.SendGlobalSMSResponse:
        """
        Sends SMS to international numbers

        Args:
            mobile_phone: Recipient phone number
            message: Message text
            country_code: Country code (e.g., "US")
            callback_url: Optional callback URL
            unicode: Unicode flag (0 or 1)
            timeout: Request timeout in seconds
        """
        url = f"{self.network}/api/message/sms/send-global"

        files = eskiz_request.SendGlobalSMSRequest(
            mobile_phone=mobile_phone,
            message=message,
            country_code=country_code,
            callback_url=callback_url,
            unicode=unicode
        ).to_file()

        headers = self.headers
        # Just make the request, we don't need the response
        self.client.request("POST", url, files=files, headers=headers, timeout=timeout)

        # Since the API returns 200 OK without a specific response body
        return eskiz_response.SendGlobalSMSResponse(success=True)

    def send_global_sms(
        self,
        mobile_phone: str,
        message: str,
        country_code: str,
        callback_url: str = "",
        unicode: str = "0",
        timeout=60
    ) -> eskiz_response.SendGlobalSMSResponse:
        """
        Sends SMS to international numbers

        Args:
            mobile_phone: Recipient phone number
            message: Message text
            country_code: Country code (e.g., "US")
            callback_url: Optional callback URL
            unicode: Unicode flag (0 or 1)
            timeout: Request timeout in seconds

        Returns:
            SendGlobalSMSResponse: Response from the API
        """
        try:
            return self._send_global_sms(
                mobile_phone, message, country_code, callback_url, unicode, timeout
            )
        except eskiz_exception.TokenExpired:
            self.login(timeout)
            return self._send_global_sms(
                mobile_phone, message, country_code, callback_url, unicode, timeout
            )

    def _get_user_messages(self, start_date: str, end_date: str, page_size: str = "20",
                          count: str = "0", is_ad: str = "", status: Optional[str] = None,
                          timeout=60) -> eskiz_response.GetUserMessagesResponse:
        """
        Retrieves user messages within a date range

        Args:
            start_date: Start date in format "YYYY-MM-DD HH:MM"
            end_date: End date in format "YYYY-MM-DD HH:MM"
            page_size: Number of results per page
            count: Count flag
            is_ad: Advertisement flag
            status: Optional status filter
            timeout: Request timeout in seconds
        """
        url = f"{self.network}/api/message/sms/get-user-messages"
        if status is not None:
            url += f"?status={status}"

        files = eskiz_request.GetUserMessagesRequest(
            start_date=start_date,
            end_date=end_date,
            page_size=page_size,
            count=count,
            is_ad=is_ad,
            status=status
        ).to_file()

        headers = self.headers
        response = self.client.request("GET", url, files=files, headers=headers, timeout=timeout)

        return eskiz_response.GetUserMessagesResponse(**response)

    def get_user_messages(self, start_date: str, end_date: str, page_size: str = "20",
                         count: str = "0", is_ad: str = "", status: Optional[str] = None,
                         timeout=60) -> eskiz_response.GetUserMessagesResponse:
        """
        Retrieves user messages within a date range

        Args:
            start_date: Start date in format "YYYY-MM-DD HH:MM"
            end_date: End date in format "YYYY-MM-DD HH:MM"
            page_size: Number of results per page
            count: Count flag
            is_ad: Advertisement flag
            status: Optional status filter
            timeout: Request timeout in seconds

        Returns:
            GetUserMessagesResponse: Response from the API
        """
        try:
            return self._get_user_messages(
                start_date, end_date, page_size, count, is_ad, status, timeout
            )
        except eskiz_exception.TokenExpired:
            self.login(timeout)
            return self._get_user_messages(
                start_date, end_date, page_size, count, is_ad, status, timeout
            )

    def _get_user_messages_by_dispatch(self, dispatch_id: str, count: str = "0",
                                      is_ad: str = "", status: Optional[str] = None,
                                      timeout=60) -> eskiz_response.GetUserMessagesResponse:
        """
        Retrieves user messages by dispatch ID

        Args:
            dispatch_id: Dispatch ID
            count: Count flag
            is_ad: Advertisement flag
            status: Optional status filter
            timeout: Request timeout in seconds
        """
        url = f"{self.network}/api/message/sms/get-user-messages-by-dispatch"
        if status is not None:
            url += f"?status={status}"

        files = eskiz_request.GetUserMessagesByDispatchRequest(
            dispatch_id=dispatch_id,
            count=count,
            is_ad=is_ad,
            status=status
        ).to_file()

        headers = self.headers
        response = self.client.request("GET", url, files=files, headers=headers, timeout=timeout)

        return eskiz_response.GetUserMessagesResponse(**response)

    def get_user_messages_by_dispatch(self, dispatch_id: str, count: str = "0",
                                     is_ad: str = "", status: Optional[str] = None,
                                     timeout=60) -> eskiz_response.GetUserMessagesResponse:
        """
        Retrieves user messages by dispatch ID

        Args:
            dispatch_id: Dispatch ID
            count: Count flag
            is_ad: Advertisement flag
            status: Optional status filter
            timeout: Request timeout in seconds

        Returns:
            GetUserMessagesResponse: Response from the API
        """
        try:
            return self._get_user_messages_by_dispatch(dispatch_id, count, is_ad, status, timeout)
        except eskiz_exception.TokenExpired:
            self.login(timeout)
            return self._get_user_messages_by_dispatch(dispatch_id, count, is_ad, status, timeout)

    def _get_dispatch_status(self, user_id: str, dispatch_id: str,
                            timeout=60) -> eskiz_response.GetDispatchStatusResponse:
        """
        Retrieves status of a dispatch

        Args:
            user_id: User ID
            dispatch_id: Dispatch ID
            timeout: Request timeout in seconds
        """
        url = f"{self.network}/api/message/sms/get-dispatch-status"

        files = eskiz_request.GetDispatchStatusRequest(
            user_id=user_id,
            dispatch_id=dispatch_id
        ).to_file()

        headers = self.headers
        response = self.client.request("GET", url, files=files, headers=headers, timeout=timeout)

        return eskiz_response.GetDispatchStatusResponse(**response)

    def get_dispatch_status(self, user_id: str, dispatch_id: str,
                           timeout=60) -> eskiz_response.GetDispatchStatusResponse:
        """
        Retrieves status of a dispatch

        Args:
            user_id: User ID
            dispatch_id: Dispatch ID
            timeout: Request timeout in seconds

        Returns:
            GetDispatchStatusResponse: Response from the API
        """
        try:
            return self._get_dispatch_status(user_id, dispatch_id, timeout)
        except eskiz_exception.TokenExpired:
            self.login(timeout)
            return self._get_dispatch_status(user_id, dispatch_id, timeout)

    def _get_message_status(
        self,
        message_id: str,
        timeout=60
    ) -> eskiz_response.MessageStatusResponse:
        """
        Retrieves status of a specific message by ID

        Args:
            message_id: Message ID
            timeout: Request timeout in seconds
        """
        url = f"{self.network}/api/message/sms/status_by_id/{message_id}"

        headers = self.headers
        response = self.client.request("GET", url, headers=headers, timeout=timeout)

        return eskiz_response.MessageStatusResponse(**response)

    def get_message_status(
        self,
        message_id: str,
        timeout=60
    ) -> eskiz_response.MessageStatusResponse:
        """
        Retrieves status of a specific message by ID

        Args:
            message_id: Message ID
            timeout: Request timeout in seconds

        Returns:
            MessageStatusResponse: Response from the API
        """
        try:
            return self._get_message_status(message_id, timeout)
        except eskiz_exception.TokenExpired:
            self.login(timeout)
            return self._get_message_status(message_id, timeout)

    def _get_templates(self, timeout=60) -> eskiz_response.TemplatesResponse:
        """
        Retrieves user templates

        Args:
            timeout: Request timeout in seconds
        """
        url = f"{self.network}/api/user/templates"

        headers = self.headers
        response = self.client.request("GET", url, headers=headers, timeout=timeout)

        return eskiz_response.TemplatesResponse(**response)

    def get_templates(self, timeout=60) -> eskiz_response.TemplatesResponse:
        """
        Retrieves user templates

        Args:
            timeout: Request timeout in seconds

        Returns:
            TemplatesResponse: Response from the API
        """
        try:
            return self._get_templates(timeout)
        except eskiz_exception.TokenExpired:
            self.login(timeout)
            return self._get_templates(timeout)

    def _export_messages(self, year: str, month: str, status: str = "all",
                        timeout=60) -> str:
        """
        Exports messages for a specific month

        Args:
            year: Year (e.g., "2025")
            month: Month (e.g., "1" for January)
            status: Status filter (default "all")
            timeout: Request timeout in seconds
        """
        url = f"{self.network}/api/message/export?status={status}"

        files = eskiz_request.ExportMessagesRequest(
            year=year,
            month=month,
            status=status
        ).to_file()

        headers = self.headers
        response = self.client.request("GET", url, files=files, headers=headers, timeout=timeout)

        # This endpoint returns CSV data as a string
        return response

    def export_messages(self, year: str, month: str, status: str = "all",
                       timeout=60) -> str:
        """
        Exports messages for a specific month

        Args:
            year: Year (e.g., "2025")
            month: Month (e.g., "1" for January)
            status: Status filter (default "all")
            timeout: Request timeout in seconds

        Returns:
            str: CSV data as a string
        """
        try:
            return self._export_messages(year, month, status, timeout)
        except eskiz_exception.TokenExpired:
            self.login(timeout)
            return self._export_messages(year, month, status, timeout)
