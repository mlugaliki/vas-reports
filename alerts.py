import psycopg2
import requests
import jsons

from connect import get_connect


def send_email(subject, body):
    url = "https://api.zeptomail.com/v1.1/email"
    payload = {
        "from": {
            "address": "noreply@guruhub.tech",
            "name": "VAS Alerts",
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


def check_hourly_results():
    try:
        print("Checking hourly results")
        data = "<table border='1'><thead><th>Delivered</th><th>Status</th><th>Service</th><th>Revenue</th></thead><body>"
        with get_connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT count(*) as delivered, o.delivery_status,s.offer_name FROM outbox o INNER JOIN services s ON o.service_id =s.id WHERE o.created_at::date >= current_date GROUP BY 2,3 ORDER BY 3;")
                rows = cur.fetchall()
                for row in rows:
                    count = row[0]
                    status = row[1]
                    revenue = 0
                    if status is None:
                        status = "Unknown"
                    if status == "DeliveryToTerminal":
                        revenue = int(count) * 10
                    data += f"<tr><td>{count}</td><td>{status}</td><td>{row[2]}</td><td>KES {revenue}</td></tr>"
        data += "</body>"
        send_email("VAS Alerts", data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error message => {error}")


check_hourly_results()
