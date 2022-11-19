import os
import logging
from datetime import datetime

import psycopg
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def main(args):
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS')

    sendgrid_key = os.getenv('SENDGRID_API_KEY')
    email_from = os.getenv("EMAIL_FROM")
    email_to = []
    email_body = ""
    should_run = False

    with psycopg.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_pass) as conn:
        # get properties from database and set database and sendgrid variables
        with conn.cursor() as cur:
            people = cur.execute('select name, dob, email, is_active from people').fetchall()

    for person in people:
        if person[3]:
            name = person[0]
            dob = str(person[1])
            birthday_date = datetime.strptime(dob, "%Y-%m-%d")
            if birthday_date.month == datetime.now().month and birthday_date.day == datetime.now().day:
                should_run = True
                age = datetime.now().year - birthday_date.year
                email_body += f"{name} was born on {dob} and is {age} years old today. Happy birthday!<br><br>"
            if person[2] is not None:
                email_to.append(person[2])

    email_body += "-- This email was automatically sent by a script because this person has a terrible memory -- "
    message = Mail(
        from_email=email_from,
        to_emails=email_to,
        subject='Happy Birthday!',
        html_content=email_body
    )

    if should_run:
        try:
            sg = SendGridAPIClient(sendgrid_key)
            response = sg.send(message)
            logging.info(response)
        except Exception as e:
            logging.error(e.message)
