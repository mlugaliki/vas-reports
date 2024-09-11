import jsons
import requests


def send_email(sender, subject, body):
    url = "https://api.zeptomail.com/v1.1/email"
    payload = {
        "from": {
            "address": "noreply@guruhub.tech",
            "name": sender,
        },
        "to": [
            {
                "email_address": {
                    "address": "mlugaliki@yahoo.com",
                    "name": "Delivery report"
                }
            }
        ],
        "subject": subject,
        "htmlbody": body
    }

    json = jsons.dumps(payload)
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'authorization': "Zoho-enczapikey wSsVR61zrEHwCv0vnDSuI+ownFgDU1qgF0973lGm4if4S/HCoMcyw0PGBVSmFfZMRzE7QjIb8O5/mxZUhGEIjYt7zVkJCCiF9mqRe1U4J3x17qnvhDzNWGhelhWILYIMwQ1tk2diEs8l+g==",
    }

    response = requests.request("POST", url, data=json, headers=headers)
    print(response.text)
