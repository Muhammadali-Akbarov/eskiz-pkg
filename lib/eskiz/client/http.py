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
    def __init__(self, token_refresh_callback=None):
        """
        Initialize the HTTP client

        Args:
            token_refresh_callback: Optional callback function to refresh token
        """
        self.token_refresh_callback = token_refresh_callback

    def request(self, method, url, headers=None, data=None, json=None, files=None, timeout=60, retry_count=0):
        """
        Use this method to send request with automatic token refresh

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            headers: Request headers
            data: Request data
            json: Request JSON data
            files: Request files
            timeout: Request timeout in seconds
            retry_count: Current retry count (used internally)
        """
        # Maximum number of retries for token refresh
        max_retries = 1

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

            # Handle token expiration with auto-refresh
            if exc.response.status_code == 401 and retry_count < max_retries:
                if self.token_refresh_callback and self.token_refresh_callback():
                    # Token refreshed successfully, retry the request
                    logger.info("Token refreshed, retrying request")
                    return self.request(
                        method, url, headers, data, json, files, timeout, retry_count + 1
                    )
                else:
                    # Token refresh failed or no callback provided
                    raise TokenExpired() from exc
            else:
                raise exc

        except Exception as exc:
            logger.error("unexpected exception: %s", exc)
            raise exc
