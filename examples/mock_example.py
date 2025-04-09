"""
Example using the mock server for testing
"""
import os
import sys
import threading
import time

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

    print("Eskiz.uz Mock Example")
    print("====================")

    # Login
    login_response = client.login()
    print("\n=== Login ===")
    print(f"Token: {login_response.data.token}")

    # Check balance
    balance = client.get_balance()
    print("\n=== Balance ===")
    print(f"Current balance: {balance} SMS")

    # Send a single SMS
    sms_response = client.send_sms(
        phone_number=998901234567,
        message="Hello from eskiz-pkg!"
    )
    print("\n=== Send SMS ===")
    print(f"SMS sent with ID: {sms_response.id}, Status: {sms_response.status}")

    # Get message status
    status_response = client.get_message_status(sms_response.id)
    print("\n=== Message Status ===")
    print(f"Message status: {status_response.data.status}")

    # Send batch SMS
    messages = [
        {"user_sms_id": "msg1", "to": 998901234567, "text": "First message"},
        {"user_sms_id": "msg2", "to": 998901234568, "text": "Second message"}
    ]
    batch_response = client.send_batch_sms(messages=messages)
    print("\n=== Send Batch SMS ===")
    print(f"Batch SMS sent with ID: {batch_response.id}, Status: {batch_response.status}")

    # Get templates
    templates_response = client.get_templates()
    print("\n=== Templates ===")
    for template in templates_response.result:
        print(f"Template ID: {template.id}, Template: {template.template}")

    # Get user messages
    messages_response = client.get_user_messages(
        start_date="2023-01-01 00:00",
        end_date="2023-12-31 23:59"
    )
    print("\n=== User Messages ===")
    print(f"Total messages: {messages_response.data.total}")
    for msg in messages_response.data.result:
        print(f"Message to {msg.to}: {msg.message} - Status: {msg.status}")

    print("\nAll examples completed!")


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
