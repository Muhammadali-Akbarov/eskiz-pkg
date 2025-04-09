"""
Mock server for testing the Eskiz.uz API client
"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler


class MockHandler(BaseHTTPRequestHandler):
    """
    Mock HTTP handler for Eskiz.uz API
    """
    def _set_headers(self, content_type="application/json", status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.send_header("Connection", "close")  # Close connection after each request
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        # Check for expired token
        auth_header = self.headers.get("Authorization", "")
        if auth_header.startswith("Bearer expired_token"):
            self._set_headers(status_code=401)
            response = {"error": "Token expired", "status": 401}
            self.wfile.write(json.dumps(response).encode())
            return

        if self.path.startswith("/api/user/get-limit"):
            self._set_headers()
            response = {
                "status": "success",
                "data": {
                    "balance": 1000
                }
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path.startswith("/api/message/sms/status_by_id/"):
            self._set_headers()
            message_id = self.path.split("/")[-1]
            response = {
                "status": "success",
                "data": {
                    "id": message_id,
                    "user_id": 1,
                    "country_id": None,
                    "connection_id": 1,
                    "smsc_id": 1,
                    "dispatch_id": None,
                    "user_sms_id": None,
                    "request_id": "abc123",
                    "price": 10,
                    "total_price": 10,
                    "is_ad": False,
                    "nick": "4546",
                    "to": "998901234567",
                    "message": "Test message",
                    "encoding": 0,
                    "parts_count": 1,
                    "parts": {},
                    "status": "delivered",
                    "smsc_data": {},
                    "template_tag": None,
                    "sent_at": "2023-01-01 12:00:00",
                    "submit_sm_resp_at": "2023-01-01 12:00:01",
                    "delivery_sm_at": "2023-01-01 12:00:02",
                    "created_at": "2023-01-01 12:00:00",
                    "updated_at": "2023-01-01 12:00:02"
                }
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path.startswith("/api/user/templates"):
            self._set_headers()
            response = {
                "success": True,
                "result": [
                    {
                        "id": 1,
                        "template": "Hello, {name}! Welcome to our service.",
                        "original_text": "Hello, {name}! Welcome to our service.",
                        "status": "active"
                    },
                    {
                        "id": 2,
                        "template": "Your verification code is {code}.",
                        "original_text": "Your verification code is {code}.",
                        "status": "active"
                    }
                ]
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path.startswith("/api/message/sms/get-user-messages"):
            self._set_headers()
            response = {
                "data": {
                    "current_page": 1,
                    "path": "/api/message/sms/get-user-messages",
                    "prev_page_url": None,
                    "first_page_url": "/api/message/sms/get-user-messages?page=1",
                    "last_page_url": "/api/message/sms/get-user-messages?page=1",
                    "next_page_url": None,
                    "per_page": 20,
                    "last_page": 1,
                    "from": 1,
                    "to": 2,
                    "total": 2,
                    "result": [
                        {
                            "id": 1,
                            "user_id": 1,
                            "country_id": None,
                            "connection_id": 1,
                            "smsc_id": 1,
                            "dispatch_id": None,
                            "user_sms_id": None,
                            "request_id": "abc123",
                            "price": 10,
                            "total_price": 10,
                            "is_ad": False,
                            "nick": "4546",
                            "to": "998901234567",
                            "message": "Test message 1",
                            "encoding": 0,
                            "parts_count": 1,
                            "parts": {},
                            "status": "delivered",
                            "smsc_data": {},
                            "template_tag": None,
                            "sent_at": "2023-01-01 12:00:00",
                            "submit_sm_resp_at": "2023-01-01 12:00:01",
                            "delivery_sm_at": "2023-01-01 12:00:02",
                            "created_at": "2023-01-01 12:00:00",
                            "updated_at": "2023-01-01 12:00:02"
                        },
                        {
                            "id": 2,
                            "user_id": 1,
                            "country_id": None,
                            "connection_id": 1,
                            "smsc_id": 1,
                            "dispatch_id": None,
                            "user_sms_id": None,
                            "request_id": "def456",
                            "price": 10,
                            "total_price": 10,
                            "is_ad": False,
                            "nick": "4546",
                            "to": "998901234568",
                            "message": "Test message 2",
                            "encoding": 0,
                            "parts_count": 1,
                            "parts": {},
                            "status": "delivered",
                            "smsc_data": {},
                            "template_tag": None,
                            "sent_at": "2023-01-02 12:00:00",
                            "submit_sm_resp_at": "2023-01-02 12:00:01",
                            "delivery_sm_at": "2023-01-02 12:00:02",
                            "created_at": "2023-01-02 12:00:00",
                            "updated_at": "2023-01-02 12:00:02"
                        }
                    ],
                    "links": []
                },
                "status": "success"
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self._set_headers()
            response = {"error": "Not implemented"}
            self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers.get("Content-Length", 0))
        # Read but don't use post_data - just to clear the buffer
        self.rfile.read(content_length)

        # Check for expired token
        auth_header = self.headers.get("Authorization", "")
        if auth_header.startswith("Bearer expired_token"):
            self._set_headers(status_code=401)
            response = {"error": "Token expired", "status": 401}
            self.wfile.write(json.dumps(response).encode())
            return

        if self.path.startswith("/api/auth/login"):
            self._set_headers()
            response = {
                "message": "token created",
                "data": {
                    "token": "mock_token_12345"
                },
                "token_type": "bearer"
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path.startswith("/api/message/sms/send"):
            self._set_headers()
            response = {
                "id": "mock-message-id-12345",
                "status": "waiting",
                "message": "SMS sent"
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path.startswith("/api/message/sms/send-batch"):
            self._set_headers()
            response = {
                "id": "mock-batch-id-12345",
                "status": ["waiting", "waiting"],
                "message": "Waiting for SMS provider"
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path.startswith("/api/message/sms/send-global"):
            self._set_headers()
            # Just return 200 OK
            response = {}
            self.wfile.write(json.dumps(response).encode())
        else:
            self._set_headers()
            response = {"error": "Not implemented"}
            self.wfile.write(json.dumps(response).encode())

    def do_PATCH(self):
        """Handle PATCH requests"""
        # Check for expired token
        auth_header = self.headers.get("Authorization", "")
        # Special case: allow token refresh even with expired token
        is_expired = auth_header.startswith("Bearer expired_token")
        is_refresh = self.path.startswith("/api/auth/refresh")
        if is_expired and is_refresh:
            self._set_headers()
            response = {
                "message": "token refreshed",
                "data": {
                    "token": "mock_refreshed_token_12345"
                },
                "token_type": "bearer"
            }
            self.wfile.write(json.dumps(response).encode())
            return

        # Handle expired token for other requests
        if auth_header.startswith("Bearer expired_token"):
            self._set_headers(status_code=401)
            response = {"error": "Token expired", "status": 401}
            self.wfile.write(json.dumps(response).encode())
            return

        if self.path.startswith("/api/auth/refresh"):
            self._set_headers()
            response = {
                "message": "token refreshed",
                "data": {
                    "token": "mock_refreshed_token_12345"
                },
                "token_type": "bearer"
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self._set_headers()
            response = {"error": "Not implemented"}
            self.wfile.write(json.dumps(response).encode())


def run_mock_server(port=8000):
    """
    Run the mock server
    """
    server_address = ("", port)
    httpd = HTTPServer(server_address, MockHandler)
    print(f"Starting mock server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run_mock_server()
