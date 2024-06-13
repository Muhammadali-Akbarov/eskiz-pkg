# Integration Eskiz.uz SMS Provider
Support Telegram - http://t.me/muhammadali_me <br>

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
   * [Auth](#auth)
   * [Refresh Token](#refresh-token)
   * [Send SMS](#send-sms)
## Auth
Example for auth get token:

Request

```
from eskiz.client.sync import ClientSync

eskiz_client = ClientSync(
    email="test@eskiz.uz",
    password="j6DWtQjjpLDNjWEk74Sx",
)

resp = eskiz_client.login()
print(resp)
```
Response
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjA4NTQ5NTUsImlhdCI6MTcxODI2Mjk1NSwicm9sZSI6InVzZXIiLCJzaWduIjoiNjU5OWQ1MWU4ZjU0NTFmMjc3OTQ1MTA3N2NmMzdmMTMxM2QzYjkzMDk1Y
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