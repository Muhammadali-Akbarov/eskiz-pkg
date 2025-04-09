<h1 align="center">Eskiz.uz SMS Integration SDK</h1>

<p align="center">
  <a href="http://t.me/muhammadali_me">
    <img src="https://img.shields.io/badge/Support-blue?logo=telegram&logoColor=white" alt="Support on Telegram"/>
  </a>
</p>

<p align="center">
  <a href="https://github.com/Muhammadali-Akbarov/eskiz-pkg"><img src="https://img.shields.io/badge/Open_Source-❤️-FDA599?"/></a>
  <a href="https://github.com/Muhammadali-Akbarov/eskiz-pkg/issues">
    <img src="https://img.shields.io/github/issues/Muhammadali-Akbarov/eskiz-pkg" />
  </a>
  <a href="https://pepy.tech/project/eskiz-pkg">
    <img src="https://static.pepy.tech/badge/eskiz-pkg" alt="PyPI - Downloads" />
  </a>
  <a href="https://pypi.org/project/eskiz-pkg/">
    <img src="https://img.shields.io/pypi/v/eskiz-pkg" alt="PyPI - Version" />
  </a>
</p>

<p align="center">Welcome to eskiz-pkg, the open source Python SDK for Eskiz.uz SMS API.</p>

<p align="center">You can use it for both synchronous and asynchronous applications with automatic token refresh.</p>
<h2 align="center">Features</h2>

<p align="center">
  <table align="center">
    <tr>
      <td align="center">✅ Sync & Async Support</td>
      <td align="center">✅ Automatic Token Refresh</td>
    </tr>
    <tr>
      <td align="center">✅ Batch SMS Sending</td>
      <td align="center">✅ International SMS</td>
    </tr>
    <tr>
      <td align="center">✅ Message Templates</td>
      <td align="center">✅ Detailed Reporting</td>
    </tr>
  </table>
</p>


## Installation

### Basic Installation
```
$ pip install eskiz-pkg
```

### With Async Support
```
$ pip install eskiz-pkg[async]
```
### Credentials
```
URL: https://notify.eskiz.uz/api/
Email: test@eskiz.uz
Password: j6DWtQjjpLDNjWEk74Sx
```

## Docs
   * [Send SMS](#send-sms)
   * [Send Batch SMS](#send-batch-sms)
   * [Send Global SMS](#send-global-sms)
   * [Get User Messages](#get-user-messages)
   * [Get User Messages by Dispatch](#get-user-messages-by-dispatch)
   * [Get Dispatch Status](#get-dispatch-status)
   * [Get Message Status](#get-message-status)
   * [Get Templates](#get-templates)
   * [Export Messages](#export-messages)
   * [Refresh Token](#refresh-token)
   * [Check Balance](#check-balance)

## Send SMS
Example for send SMS:

Request

```
from eskiz.client.sync import ClientSync

eskiz_client = ClientSync(
    email="test@eskiz.uz",
    password="j6DWtQjjpLDNjWEk74Sx",
)

text = "Hello from Python"

resp = eskiz_client.send_sms(
    phone_number=998888351717,
    message=text
)

print(resp)
```
Response

```
id='e837dec2-2f5a-44a9-a1d1-6fcc13e94d86' message='Waiting for SMS provider' status='waiting'
```


## Refresh Token
Example for refresh token:

Request

```
from eskiz.client.sync import ClientSync

eskiz_client = ClientSync(
    email="test@eskiz.uz",
    password="j6DWtQjjpLDNjWEk74Sx",
)

resp = eskiz_client.refresh_token()
print(resp)
```
Response

```
eyJleHAiOjE3MjA4NTQ5NTUsImlhdCI6MTcxODI2Mjk1NSwicm9sZSI6InVzZXIiLCJzaWduIjoiNjU5OWQ1MWU4ZjU0NTFmMjc3OTQ1MTA3N2NmMzdmMTMxM2QzYjkzMDk1Y
```

## Check Balance
Example for checking the SMS balance:

Request

```
from eskiz.client.sync import ClientSync

eskiz_client = ClientSync(
    email="test@eskiz.uz",
    password="j6DWtQjjpLDNjWEk74Sx",
)

balance = eskiz_client.get_balance()
print(f"Remaining SMS credits: {balance}")
```
Response

```
Remaining SMS credits: 0
```

## Send Batch SMS
Example for sending multiple SMS messages in a single request:

Request

```python
from eskiz.client.sync import ClientSync

eskiz_client = ClientSync(
    email="test@eskiz.uz",
    password="j6DWtQjjpLDNjWEk74Sx",
)

messages = [
    {"user_sms_id": "msg1", "to": 998888351717, "text": "Hello from Python 1"},
    {"user_sms_id": "msg2", "to": 998888351718, "text": "Hello from Python 2"}
]

resp = eskiz_client.send_batch_sms(
    messages=messages,
    dispatch_id=123  # Optional
)

print(resp)
```

Response

```
id='9309c090-8bc5-4fae-9d82-6b84af55affe' message='Waiting for SMS provider' status=['waiting', 'waiting']
```

## Send Global SMS
Example for sending SMS to international numbers:

Request

```python
from eskiz.client.sync import ClientSync

eskiz_client = ClientSync(
    email="test@eskiz.uz",
    password="j6DWtQjjpLDNjWEk74Sx",
)

resp = eskiz_client.send_global_sms(
    mobile_phone="12025550123",  # US number
    message="Hello from Python",
    country_code="US"
)

print(resp)
```

Response

```
success=True
```

## Get User Messages
Example for retrieving user messages within a date range:

Request

```python
from eskiz.client.sync import ClientSync

eskiz_client = ClientSync(
    email="test@eskiz.uz",
    password="j6DWtQjjpLDNjWEk74Sx",
)

resp = eskiz_client.get_user_messages(
    start_date="2023-11-01 00:00",
    end_date="2023-11-02 23:59",
    page_size="20"
)

print(f"Total messages: {resp.data.total}")
for msg in resp.data.result:
    print(f"Message to {msg.to}: {msg.message} - Status: {msg.status}")
```

## Get User Messages by Dispatch
Example for retrieving user messages by dispatch ID:

Request

```python
from eskiz.client.sync import ClientSync

eskiz_client = ClientSync(
    email="test@eskiz.uz",
    password="j6DWtQjjpLDNjWEk74Sx",
)

resp = eskiz_client.get_user_messages_by_dispatch(
    dispatch_id="123"
)

print(f"Total messages: {resp.data.total}")
for msg in resp.data.result:
    print(f"Message to {msg.to}: {msg.message} - Status: {msg.status}")
```

## Get Dispatch Status
Example for retrieving status of a dispatch:

Request

```python
from eskiz.client.sync import ClientSync

eskiz_client = ClientSync(
    email="test@eskiz.uz",
    password="j6DWtQjjpLDNjWEk74Sx",
)

resp = eskiz_client.get_dispatch_status(
    user_id="1",
    dispatch_id="123"
)

for status_item in resp.data:
    print(f"Status: {status_item.status}, Total: {status_item.total}")
```

## Get Message Status
Example for retrieving status of a specific message by ID:

Request

```python
from eskiz.client.sync import ClientSync

eskiz_client = ClientSync(
    email="test@eskiz.uz",
    password="j6DWtQjjpLDNjWEk74Sx",
)

resp = eskiz_client.get_message_status(
    message_id="c779e2c3-9140-4b0f-862d-ee5639c3f5e0"
)

print(f"Message to {resp.data.to}: {resp.data.message} - Status: {resp.data.status}")
```

## Get Templates
Example for retrieving user templates:

Request

```python
from eskiz.client.sync import ClientSync

eskiz_client = ClientSync(
    email="test@eskiz.uz",
    password="j6DWtQjjpLDNjWEk74Sx",
)

resp = eskiz_client.get_templates()

for template in resp.result:
    print(f"Template ID: {template.id}, Template: {template.template}")
```

## Export Messages
Example for exporting messages for a specific month:

Request

```python
from eskiz.client.sync import ClientSync

eskiz_client = ClientSync(
    email="test@eskiz.uz",
    password="j6DWtQjjpLDNjWEk74Sx",
)

csv_data = eskiz_client.export_messages(
    year="2025",
    month="1"
)

# Save to file
with open("messages_export.csv", "w") as f:
    f.write(csv_data)

print("Export saved to messages_export.csv")
```

## Async Client
The library also provides an async client for use with modern Python applications using asyncio.

### Basic Usage

```python
import asyncio
from eskiz.client import AsyncClient

async def main():
    async with AsyncClient(
        email="test@eskiz.uz",
        password="j6DWtQjjpLDNjWEk74Sx",
    ) as client:
        # Send SMS
        response = await client.send_sms(
            phone_number=998888351717,
            message="Hello from Python"
        )
        print(response)

        # Check balance
        balance = await client.get_balance()
        print(f"Balance: {balance}")

asyncio.run(main())
```

### Sending Batch SMS with Async Client

```python
import asyncio
from eskiz.client import AsyncClient

async def main():
    async with AsyncClient(
        email="test@eskiz.uz",
        password="j6DWtQjjpLDNjWEk74Sx",
    ) as client:
        messages = [
            {"user_sms_id": "msg1", "to": 998888351717, "text": "Hello from Python 1"},
            {"user_sms_id": "msg2", "to": 998888351718, "text": "Hello from Python 2"}
        ]

        response = await client.send_batch_sms(messages=messages)
        print(response)

asyncio.run(main())
```
