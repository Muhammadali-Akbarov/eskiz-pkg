"""
the http client
"""
import logging
import requests

from requests.exceptions import HTTPError

from eskiz.exception import TokenExpired


logger = logging.getLogger(__name__)


class HttpClient:
    """
    A simple HTTP client to handle requests.
    """
    @staticmethod
    def request(method, url, headers=None, data=None, json=None, files=None, timeout=60):
        """
        Use this method to send request
        """
        kwargs = {
            "method": method,
            "url": url,
            "headers": headers,
            "data": data,
            "files": files,
            "json": json,
            "timeout": timeout
        }

        try:
            response = requests.request(**kwargs)
            response.raise_for_status()
            response = response.json()
            return response

        except HTTPError as exc:
            logger.error("HTTP error: %s", exc)

            if exc.response.status_code == 401:
                raise TokenExpired() from exc

            raise exc

        except Exception as exc:
            logger.error("unexpected exception: %s", exc)
            raise exc
