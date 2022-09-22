import logging

from requests import request

logger = logging.getLogger(__name__)


class SMSClient:
    __GET = 'get'
    __POST = "post"
    __PATCH = "patch"
    __CONTACT = "contact"

    def __init__(
        self,
        api_url: str,
        email: str,
        password: str,
        callback_url: str = None,
    ) -> None:
        self.__api_url = api_url
        self.__email = email
        self.__password = password
        self.__callback_url = callback_url
        self.__headers = {}

        self.__methods: dict = {
            "auth_user": "auth/user",
            "auth_login": "auth/login",
            "auth_refresh": "auth/refresh",
            "send_message": "message/sms/send"
        }

    def __request(self, api_path: str, data: dict = None, **kwargs):
        """Use this method to send request"""
        incoming_data: dict = {"status": "error"}
        req_data: dict = {
            "data": data,
            "method": kwargs.pop("method"),
            "headers": kwargs.pop("headers", None),
            "url": self.__api_url + api_path
        }

        try:
            resp = request(**req_data)
            if api_path == self.__methods['auth_refresh']:
                if resp.status_code == 200:
                    incoming_data["status"] = "success"
            else:
                incoming_data = resp.json()
        except Exception as error:
            mess: str = """
            Error while sending request\n
            api_path: {api_url},
            data: {data},
            error: {error}
            """
            err: str = mess.format(
                api_url=req_data.get("url"),
                data=req_data.get("req_data"),
                error=error
            )
            logger.error(err)

        return incoming_data

    def _auth(self) -> dict:
        """Use this API for authorization, returns a token"""
        data: dict = {
            "method": self.__POST,
            "api_path": self.__methods.get("auth_login"),
            "data": {
                "email": self.__email,
                "password": self.__password
            }
        }
        return self.__request(**data)

    def _refresh_token(self) -> dict:
        """Delete current token"""
        token: str = self._auth().get('data').get('token')
        self.__headers["Authorization"] = f"Bearer {token}"

        context: dict = {
            "headers": self.__headers,
            "method": self.__PATCH,
            "api_path": self.__methods.get("auth_refresh"),
        }

        return self.__request(**context)

    def _get_my_user_info(self) -> dict:
        """Returns all user data"""
        token: str = self._auth().get('data').get('token')
        self.__headers["Authorization"] = f"Bearer {token}"

        data: dict = {
            "method": self.__GET,
            "headers": self.__headers,
            "api_path": self.__methods.get("auth_user")
        }

        return self.__request(**data)

    def _add_sms_contact(
        self,
        first_name: str,
        phone_number: str,
        group: str,
    ) -> dict:
        """Add contact to Data Base.

        :param first_name: string: First Name of the contact
        :param phone_number: string: Phone Number of the contact
        :param group: string: Group for the contacts
        """
        token: str = self._auth().get('data').get('token')
        self.__headers["Authorization"] = f"Bearer {token}"

        data: dict = {
            "method": self.__POST,
            "headers": self.__headers,
            "api_path": self.__CONTACT,
            "data": {
                "name": first_name,
                "email": self.__email,
                "group": group,
                "mobile_phone": phone_number,
            }
        }
        return self.__request(**data)

    def _send_sms(self, phone_number: str, message: str) -> dict:
        """Use this method to send sms message.

        :param phone_number: string: Phone Number max length 12 char without +
        :param message: string: Message(Text)
        """
        token: str = self._auth().get('data').get('token')
        self.__headers["Authorization"] = f"Bearer {token}"

        data: dict = {
            "method": self.__POST,
            "headers": self.__headers,
            "api_path": self.__methods.get("send_message"),
            "data":  {
                "from": 4546,
                "mobile_phone": phone_number,
                "callback_url": self.__callback_url,
                "message": message
            }
        }
        return self.__request(**data)


