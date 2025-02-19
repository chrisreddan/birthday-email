import logging
import os
from datetime import datetime

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_mail(message: Mail) -> None:
    try:
        sendgrid_key = os.getenv("SENDGRID_API_KEY")
        sg = SendGridAPIClient(sendgrid_key)
        response = sg.send(message)
        logging.info(response)
    except Exception as e:
        logging.error(f"Error running process: {e}")


def build_mail(people: iter) -> tuple[bool, Mail]:
    email_from = os.getenv("EMAIL_FROM")
    email_to = []
    email_body = ""
    has_birthday = False

    for person in people:
        if person['is_active']:
            name = person['name']
            dob = str(person['dob'])
            birthday_date = datetime.strptime(dob, "%Y-%m-%d")
            current_date = datetime.now()

            if person['email'] is not None:
                email_to.append(person['email'])

            if birthday_date.month == current_date.month and birthday_date.day == current_date.day:
                has_birthday = True
                age = current_date.year - birthday_date.year
                email_body += f"{name} was born on {dob} and is {age} years old today. Happy birthday!<br><br>"

    email_body += "-- This email was automatically sent because this person has a terrible memory -- "

    mail = Mail(
        from_email=email_from,
        to_emails=email_to,
        subject='Happy Birthday!',
        html_content=email_body
    )

    return has_birthday, mail


def main(args):
    people = args.get("people")
    has_birthday, mail = build_mail(people)

    if has_birthday:
        send_mail(mail)
