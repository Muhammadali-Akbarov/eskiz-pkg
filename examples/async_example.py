"""
Example usage of the asynchronous client
"""
import os
import sys
import asyncio

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now import the modules
from eskiz.client import AsyncClient  # noqa: E402


async def send_sms_example(client):
    """Example of sending a single SMS"""
    print("\n=== Sending Single SMS ===")
    response = await client.send_sms(
        phone_number=998901234567,  # Replace with a real number
        message="Hello from eskiz-pkg async!"
    )
    print(f"SMS sent with ID: {response.id}, Status: {response.status}")
    return response.id


async def send_batch_sms_example(client):
    """Example of sending batch SMS"""
    print("\n=== Sending Batch SMS ===")
    messages = [
        {"user_sms_id": "msg1", "to": 998901234567, "text": "First message"},
        {"user_sms_id": "msg2", "to": 998901234568, "text": "Second message"}
    ]
    response = await client.send_batch_sms(messages=messages)
    print(f"Batch SMS sent with ID: {response.id}, Status: {response.status}")
    return response.id


async def send_global_sms_example(client):
    """Example of sending international SMS"""
    print("\n=== Sending Global SMS ===")
    response = await client.send_global_sms(
        mobile_phone="12025550123",  # US number
        message="Hello from Python",
        country_code="US"
    )
    print(f"Global SMS sent successfully: {response.success}")


async def check_balance_example(client):
    """Example of checking balance"""
    print("\n=== Checking Balance ===")
    balance = await client.get_balance()
    print(f"Current balance: {balance} SMS")


async def get_message_status_example(client, message_id):
    """Example of getting message status"""
    print("\n=== Getting Message Status ===")
    try:
        status = await client.get_message_status(message_id)
        print(f"Message status: {status.data.status}")
    except Exception as e:
        print(f"Error getting message status: {e}")


async def get_templates_example(client):
    """Example of getting templates"""
    print("\n=== Getting Templates ===")
    try:
        templates = await client.get_templates()
        if templates.result:
            for template in templates.result[:3]:  # Show first 3 templates
                print(f"Template ID: {template.id}, Template: {template.template[:30]}...")
        else:
            print("No templates found")
    except Exception as e:
        print(f"Error getting templates: {e}")


async def main():
    """
    Main function demonstrating the usage of the asynchronous client
    """
    print("Eskiz.uz Async Client Example")
    print("============================")

    # Initialize client using async context manager
    async with AsyncClient(
        email="your_email@example.com",  # Replace with your credentials
        password="your_password",
        from_="4546",  # Your sender ID
    ) as client:
        # Check balance
        await check_balance_example(client)

        # Send a single SMS and get its ID
        message_id = await send_sms_example(client)

        # Get message status
        await get_message_status_example(client, message_id)

        # Send batch SMS
        await send_batch_sms_example(client)

        # Send global SMS
        await send_global_sms_example(client)

        # Get templates
        await get_templates_example(client)

        print("\nAll examples completed!")


if __name__ == "__main__":
    asyncio.run(main())
