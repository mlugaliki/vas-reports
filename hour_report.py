from datetime import datetime

import psycopg2

from connect import get_connect
from vas_email import send_email


def hourly_deliveries():
    try:
        print("Checking hourly deliveries")
        data = ""
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
                    data += (
                        f"<tr><td style=\"border-collapse: collapse; border: 1px solid #cccccc;  padding:5px;\">{count}</td>"
                        f"<td style=\"border-collapse: collapse; border: 1px solid #cccccc;  padding:5px;\">{status}</td>"
                        f"<td style=\"border-collapse: collapse; border: 1px solid #cccccc;  padding:5px;\">{row[2]}</td>"
                        f"<td style=\"border-collapse: collapse; border: 1px solid #cccccc;  padding:5px;\">KES {revenue}</td>"
                        f"</tr>")
        return data
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error message => {error}")


def hourly_subscription():
    try:
        print("Checking hourly subscription")
        data = ""
        with get_connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT count(*), sv.offer_name,s.subscription_type FROM subscriptions s INNER JOIN services sv ON s.service_id=sv.id GROUP BY 2,3 ORDER BY 3;")
                rows = cur.fetchall()
                for row in rows:
                    count = row[0]
                    service_name = row[1]
                    subscription_type = row[2]
                    data += (
                        f"<tr><td style=\"border-collapse: collapse; border: 1px solid #cccccc; padding:5px;\">{count}</td>"
                        f"<td style=\"border-collapse: collapse; border: 1px solid #cccccc; padding: 5px;\">{service_name}</td>"
                        f"<td style=\"border-collapse: collapse; border: 1px solid #cccccc; padding: 5px;\">{subscription_type}</td>"
                        f"</tr>")
        return data
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error message => {error}")


def send_hourly_deliveries():
    time = datetime.now()
    sms = hourly_deliveries()
    file1 = open("hourly-template.html", "r+")
    template = file1.read()
    template = template.replace("{DATE}", time.strftime("%b %d, %Y @ %H"))
    file1.close()
    body = template.replace("{DELIVERIES}", sms)

    subscribers = hourly_subscription()
    body = body.replace("{SUBSCRIPTIONS}", subscribers)
    send_email("Report Service", "Hourly Report", body)


send_hourly_deliveries()
