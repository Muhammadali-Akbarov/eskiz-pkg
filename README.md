# Integration Eskiz.uz SMS Provider
Support by Telegram - http://t.me/muhammadali_me <br>

```
$ pip install eskiz-pkg
```
### Credentials
```
URL: https://notify.eskiz.uz/api/
Email: test@eskiz.uz
Password: j6DWtQjjpLDNjWEk74Sx
```

## Docs
   * [Send SMS](#send-sms)
   * [Refresh Token](#refresh-token)

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
