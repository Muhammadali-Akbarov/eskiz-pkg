"""
Example demonstrating the auto token refresh feature
"""
import os
import sys
import time
import threading

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now import the modules
from eskiz.client.sync import ClientSync  # noqa: E402
from tests.mock_server import run_mock_server  # noqa: E402


def run_example():
    """
    Run the example with the mock server
    """
    # Initialize client with mock server URL
    client = ClientSync(
        email="test@example.com",
        password="password",
        network="http://localhost:8765"
    )

    print("Eskiz.uz Token Refresh Example")
    print("=============================")

    # Login
    login_response = client.login()
    print("\n=== Initial Login ===")
    print(f"Token: {login_response.data.token}")

    # Store the initial token
    initial_token = client.token

    # Check balance
    balance = client.get_balance()
    print("\n=== Balance Check with Initial Token ===")
    print(f"Current balance: {balance} SMS")

    # Simulate token expiration by manually changing the token
    print("\n=== Simulating Token Expiration ===")
    client.token = "expired_token"
    client.headers["Authorization"] = f"Bearer {client.token}"
    print(f"Changed token to: {client.token}")

    # Try to send SMS with expired token - this should trigger auto refresh
    try:
        print("\n=== Sending SMS with Expired Token ===")
        print("This should trigger automatic token refresh...")
        sms_response = client.send_sms(
            phone_number=998901234567,
            message="Hello from eskiz-pkg with auto token refresh!"
        )
        print(f"SMS sent with ID: {sms_response.id}, Status: {sms_response.status}")

        # Check if token was refreshed
        print("\n=== Token Refresh Check ===")
        print(f"Initial token: {initial_token}")
        print(f"Current token: {client.token}")
        print(f"Token was {'refreshed' if initial_token != client.token else 'not refreshed'}")

    except Exception as e:
        print(f"Error: {e}")

    print("\nExample completed!")


if __name__ == "__main__":
    # Start the mock server in a separate thread
    mock_server_thread = threading.Thread(
        target=run_mock_server,
        args=(8765,),
        daemon=True
    )
    mock_server_thread.start()

    # Give the server time to start
    time.sleep(1)

    # Run the example
    run_example()
