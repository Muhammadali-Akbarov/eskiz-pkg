"""
the http syns client
"""
from eskiz.enum import Network
from eskiz.client.http import HttpClient
from eskiz import request as eskiz_request
from eskiz import response as eskiz_response
from eskiz import exception as eskiz_exception


class ClientSync:
    """
    The Eskiz HTTP sync client
    """
    def __init__(
        self,
        email: str,
        password: str,
        network: str = Network.MAIN,
        client: HttpClient = HttpClient(),
        from_: str = "4546",
        callback: str = "",
    ):
        self.from_ = from_
        self.email = email
        self.password = password
        self.network = network
        self.client = client
        self.callback = callback
        self.headers = {}
        response = self.login()
        self.token = response.data.token
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
        """
        url = f"{self.network}/api/auth/refresh"

        headers = self.headers
        response = self.client.request("PATCH", url, headers=headers, timeout=timeout)

        return eskiz_response.RefreshTokenResponse(**response)

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
