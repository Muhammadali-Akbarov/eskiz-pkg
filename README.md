# Integration Eskiz SMS API with Python | SMS Service 
Sourcode and Resources for Eskiz & Python <hr>
Support Telegram - http://t.me/muhammadali_me <br>
Documentation & More https://documenter.getpostman.com/view/663428/RzfmES4z?version=latest<br>
<hr>
<p align="center">
    <img style="width: 100%;" src="https://telegra.ph/file/2717ca1f2e52df46df06d.png"></img> </hr>
</p>

## Getting started
There are two ways to install the library:

* Installation using pip (a Python package manager):

```
$ pip install eskiz-pkg
```
* Installation from source (requires git):

```
$ git clone https://github.com/Muhammadali-Akbarov/eskiz-pkg
$ cd eskiz-pkg
$ python setup.py install
```
or:
```
$ pip install git+https://github.com/Muhammadali-Akbarov/eskiz-pkg
```

### Library Structure
```
└── eskiz
    ├── client.py
    └── __init__.py
```
### Credentials
```
URL: https://notify.eskiz.uz/api/
Email: test@eskiz.uz
Password: j6DWtQjjpLDNjWEk74Sx
```

## Doc

  * [Getting Started](#getting-started)
  * Auth
    * [Auth](#auth)
    * [Refresh Token](#refresh-token)
   
  * Users
    * [Add Contact](#add-contact)
  * SMS
    * [Send SMS](#send-sms)
## Auth
Example for auth get token:

Request

```
from pprint import pprint

from eskiz.client import SMSClient


client = SMSClient(
    api_url="https://notify.eskiz.uz/api/",
    email="test@eskiz.uz",
    password="j6DWtQjjpLDNjWEk74Sx",
)

resp = client._auth()
pprint(resp)
```
Response

```
{
    "message": "token_generated",
    "data": {
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjUwOCwicm9sZSI6InVzZXIiLCJkYXRhIjp7ImlkIjo1MDgsIm5hbWUiOiJPT08gU01BUlQgUklWT0pMQU5JU0ggTUFSS0FaSSIsImVtYWlsIjoiYXRhZGppdGRpbm92QGdtYWlsLmNvbSIsInJvbGUiOiJ1c2VyIiwiYXBpX3Rva2VuIjoiZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6STFOaUo5LmV5SnpkV0lpT2pVd09Dd2ljbTlzWlNJNkluVnpaWElpTENKa1lYUmhJanA3SW1sa0lqbzFNRGdzSW01aGJXVWlPaUpQVDA4Z1UwMUJVbFFnVWtsV1QwcE1RVTVKVTBnZ1RVRlNTMEZhU1NJc0ltVnRZV2xzSWpvaVlYUmhaR3BwZEdScGJtOTJRR2R0WVdsc0xtTnZiU0lzSW5KdmJHVWlPaUoxYzJWeUlpd2lZWEJwWDNSdmEyVnVJam9pWlhsS01HVllRV2xQYVVwTFZqRlJhVXhEU21oaVIyIiwic3RhdHVzIjoiYWN0aXZlIiwic21zX2FwaV9sb2dpbiI6ImVza2l6MiIsInNtc19hcGlfcGFzc3dvcmQiOiJlJCRrIXoiLCJ1el9wcmljZSI6NTAsInVjZWxsX3ByaWNlIjo1MCwiYmFsYW5jZSI6ODgxMjUsImlzX3ZpcCI6MCwiaG9zdCI6InNlcnZlcjEiLCJjcmVhdGVkX2F0IjoiMjAyMS0wNS0wOVQxMjo0NzoxNi4wMDAwMDBaIiwidXBkYXRlZF9hdCI6IjIwMjItMDktMjFUMTQ6MzA6MDIuMDAwMDAwWiJ9LCJpYXQiOjE2NjM4MjM0NjAsImV4cCI6MTY2NjQxNTQ2MH0.mrqsquTf9PJ_sjVHW7J3ysHTXEZG4M67IWuXsuM75v8"
    },
    "token_type": "bearer"
}
```
## Refresh Token
Example for refresh token:

Request

```
from pprint import pprint

from eskiz.client import SMSClient


client = SMSClient(
    api_url="https://notify.eskiz.uz/api/",
    email="test@eskiz.uz",
    password="j6DWtQjjpLDNjWEk74Sx",
)

resp = client._refresh_token()
pprint(resp)

```
Response

```
{'status': 'success'}
```
## Add Contact
Example for add user info to contact list:

Request

```
from pprint import pprint

from eskiz.client import SMSClient


client = SMSClient(
    api_url="https://notify.eskiz.uz/api/",
    email="test@eskiz.uz",
    password="j6DWtQjjpLDNjWEk74Sx",
)

resp = client._add_sms_contact(
    first_name="Muhammadali",
    phone_number="998888351717",
    group="test"
)
pprint(resp)
```
Response

```
{
    "status": "success",
    "data": {
      "contact_id": 250812
    }
}
```
## Send SMS
Example for send SMS:

Request

```
from pprint import pprint

from eskiz.client import SMSClient


client = SMSClient(
    api_url="https://notify.eskiz.uz/api/",
    email="test@eskiz.uz",
    password="j6DWtQjjpLDNjWEk74Sx",
)

resp = client._send_sms(
    phone_number="998888351717",
    message="Hello from Python❤️"
)
pprint(resp)
```
Response

```
{
    "id": "59f0e35a-2c73-4726-a232-3d4050174315",
    "status": "waiting",
    "message": "Waiting for SMS provider"
}
```
