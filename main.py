from lib.eskiz.client import SMSClient


client = SMSClient(
    api_url="https://notify.eskiz.uz/api/",
    email="test@eskiz.uz",
    password="j6DWtQjjpLDNjWEk74Sx",
)

resp = client._send_sms(
    phone_number="998888351717",
    message="Hello from Python ❤️",
)
print(resp)
