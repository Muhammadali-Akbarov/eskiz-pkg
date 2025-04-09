"""
Example using the mock server for testing the async client
"""
import os
import sys
import asyncio
import threading
import time

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now import the modules
from eskiz.client import AsyncClient  # noqa: E402
from tests.mock_server import run_mock_server  # noqa: E402


async def run_async_example():
    """
    Run the async example with the mock server
    """
    print("Eskiz.uz Async Mock Example")
    print("==========================")

    # Initialize client with mock server URL
    async with AsyncClient(
        email="test@example.com",
        password="password",
        network="http://localhost:8765"
    ) as client:
        # Check balance
        balance = await client.get_balance()
        print("\n=== Balance ===")
        print(f"Current balance: {balance} SMS")

        # Send a single SMS
        sms_response = await client.send_sms(
            phone_number=998901234567,
            message="Hello from eskiz-pkg async!"
        )
        print("\n=== Send SMS ===")
        print(f"SMS sent with ID: {sms_response.id}, Status: {sms_response.status}")

        # Send batch SMS
        messages = [
            {"user_sms_id": "msg1", "to": 998901234567, "text": "First message"},
            {"user_sms_id": "msg2", "to": 998901234568, "text": "Second message"}
        ]
        batch_response = await client.send_batch_sms(messages=messages)
        print("\n=== Send Batch SMS ===")
        print(f"Batch SMS sent with ID: {batch_response.id}, Status: {batch_response.status}")

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
    asyncio.run(run_async_example())
