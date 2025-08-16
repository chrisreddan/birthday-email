import os
import logging
from datetime import datetime

from postmarker.core import PostmarkClient


def main(args):
    current_date = datetime.now()
    email_to = []
    email_body = ""
    is_birthday = False
    people = args.get("people")

    for person in people:
        if person['is_active']:
            name = person['name']
            dob = str(person['dob'])
            birthday_date = datetime.strptime(dob, "%Y-%m-%d")
            if birthday_date.month == current_date.month and birthday_date.day == current_date.day:
                is_birthday = True
                age = current_date.year - birthday_date.year
                email_body += f"{name} was born on {dob} and is {age} years old today. Happy email!<br><br>"
            if person['email'] is not None:
                email_to.append(person['email'])

    email_body += "-- This email was automatically sent because this person has a terrible memory -- "

    if is_birthday:
        try:
            email_from = os.getenv("EMAIL_FROM")
            api_token = os.getenv("POSTMARK_API_TOKEN")
            logging.error(f"Sending email to {email_to}")
            logging.error(f"Token = {api_token}")
            postmark = PostmarkClient(api_token)
            postmark.emails.send(From=email_from, To=email_to, Subject='Happy Birthday!', HtmlBody=email_body)
            logging.info("Email sent")
        except Exception as e:
            logging.error(f"Error running process: {e}")
