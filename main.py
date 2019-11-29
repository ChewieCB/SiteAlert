import sys
import imaplib
import email

import yaml
from twilio.rest import Client
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

test_bin = ""     # TODO: add a bin for status response data when its working


@sched.scheduled_job('interval', minutes=1)
def get_inbox():
    """

    :return:
    """
    mail_credentials = config["generators gmail"]

    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(mail_credentials["username"], mail_credentials["password"])
    mail.select('Inbox')
    stringers_type, stringers_data = mail.search(None, '(FROM "stringershydro@hallidays.com" UNSEEN)')

    unseen_scenarios = []

    # TODO: add logic for splitting the scenarios into a site-separated dict
    for num in stringers_data[0].split():
        typ, data = mail.fetch(num, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode('utf-8'))
                scenario = msg['subject'].split('Stringers ')[1]
                unseen_scenarios.append(scenario)

    if unseen_scenarios:
        [send_alert("Stringer's Weir", scenario) for scenario in unseen_scenarios]
        sys.stdout.write(f"\n{len(unseen_scenarios)} alerts sent.")
        sys.stdout.write(f"\n\tSite: Stringer's Weir")
        [sys.stdout.write(f"\n\tAlert: {scenario}") for scenario in unseen_scenarios]
    # else:
        # sys.stdout.write("\nNo unseen alerts.")


def send_alert(site, scenario):
    """

    :return:
    """
    twilio_credentials = config["twilio"]
    personal_numbers = config["personal numbers"]

    call_list = personal_numbers.values()

    body_message = f"\n\n{site} alert:\n{scenario}."

    client = Client(twilio_credentials["SID"], twilio_credentials["TOKEN"])
    [client.messages.create(
        to=number,
        from_=twilio_credentials["TRIAL_NUMBER"],
        body=body_message,
        status_callback=test_bin,
    ) for number in call_list]


if __name__ == "__main__":

    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    sched.start()
