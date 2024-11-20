import os
import logging
from datetime import datetime

import psycopg
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def main(args):

    sendgrid_key = os.getenv("SENDGRID_API_KEY")
    email_from = os.getenv("EMAIL_FROM")
    email_to = []
    email_body = ""
    should_run = False
    people = args.get("people")
    
    for person in people:
        if person['is_active']:
            name = person['name']
            dob = str(person['dob'])
            birthday_date = datetime.strptime(dob, "%Y-%m-%d")
            if birthday_date.month == datetime.now().month and birthday_date.day == datetime.now().day:
                should_run = True
                age = datetime.now().year - birthday_date.year
                email_body += f"{name} was born on {dob} and is {age} years old today. Happy birthday!<br><br>"
            if person['email'] is not None:
                email_to.append(person['email'])

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
