"""
Example usage of the synchronous client
"""
import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now import the modules
from eskiz.client.sync import ClientSync  # noqa: E402


def send_sms_example(client):
    """Example of sending a single SMS"""
    print("\n=== Sending Single SMS ===")
    response = client.send_sms(
        phone_number=998901234567,  # Replace with a real number
        message="Hello from eskiz-pkg!"
    )
    print(f"SMS sent with ID: {response.id}, Status: {response.status}")
    return response.id


def send_batch_sms_example(client):
    """Example of sending batch SMS"""
    print("\n=== Sending Batch SMS ===")
    messages = [
        {"user_sms_id": "msg1", "to": 998901234567, "text": "First message"},
        {"user_sms_id": "msg2", "to": 998901234568, "text": "Second message"}
    ]
    response = client.send_batch_sms(messages=messages)
    print(f"Batch SMS sent with ID: {response.id}, Status: {response.status}")
    return response.id


def send_global_sms_example(client):
    """Example of sending international SMS"""
    print("\n=== Sending Global SMS ===")
    response = client.send_global_sms(
        mobile_phone="12025550123",  # US number
        message="Hello from Python",
        country_code="US"
    )
    print(f"Global SMS sent successfully: {response.success}")


def check_balance_example(client):
    """Example of checking balance"""
    print("\n=== Checking Balance ===")
    balance = client.get_balance()
    print(f"Current balance: {balance} SMS")


def get_message_status_example(client, message_id):
    """Example of getting message status"""
    print("\n=== Getting Message Status ===")
    try:
        status = client.get_message_status(message_id)
        print(f"Message status: {status.data.status}")
    except Exception as e:
        print(f"Error getting message status: {e}")


def get_templates_example(client):
    """Example of getting templates"""
    print("\n=== Getting Templates ===")
    try:
        templates = client.get_templates()
        if templates.result:
            for template in templates.result[:3]:  # Show first 3 templates
                print(f"Template ID: {template.id}, Template: {template.template[:30]}...")
        else:
            print("No templates found")
    except Exception as e:
        print(f"Error getting templates: {e}")


def get_user_messages_example(client):
    """Example of getting user messages"""
    print("\n=== Getting User Messages ===")
    try:
        # Use fixed dates for the example
        start_date = "2023-01-01 00:00"
        end_date = "2023-12-31 23:59"

        messages = client.get_user_messages(
            start_date=start_date,
            end_date=end_date,
            page_size="5"  # Limit to 5 messages
        )

        print(f"Total messages: {messages.data.total}")
        for msg in messages.data.result[:3]:  # Show first 3 messages
            print(f"Message to {msg.to}: {msg.message[:30]}... - Status: {msg.status}")
    except Exception as e:
        print(f"Error getting user messages: {e}")


def main():
    """
    Main function demonstrating the usage of the synchronous client
    """
    print("Eskiz.uz Sync Client Example")
    print("===========================")

    # Initialize client
    client = ClientSync(
        email="your_email@example.com",  # Replace with your credentials
        password="your_password",
        from_="4546",  # Your sender ID
    )

    # Login (automatically called when needed, but can be called explicitly)
    client.login()

    # Check balance
    check_balance_example(client)

    # Send a single SMS and get its ID
    message_id = send_sms_example(client)

    # Get message status
    get_message_status_example(client, message_id)

    # Send batch SMS
    send_batch_sms_example(client)

    # Send global SMS
    send_global_sms_example(client)

    # Get templates
    get_templates_example(client)

    # Get user messages
    get_user_messages_example(client)

    print("\nAll examples completed!")


if __name__ == "__main__":
    main()
