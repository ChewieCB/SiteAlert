import sys
import imaplib
import email

from twilio.rest import Client
from apscheduler.schedulers.blocking import BlockingScheduler

import credentials

sched = BlockingScheduler()

test_bin = ""     # TODO: add a bin for status response data when its working


@sched.scheduled_job('interval', minutes=1)
def get_inbox():
    """

    :return:
    """
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(credentials.gen_user, credentials.gen_pass)
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
        [sys.stdout.write(f"\n\n\tSite: Stringer's Weir\n\tAlert: {scenario}") for scenario in unseen_scenarios]
    else:
        sys.stdout.write("\nNo unseen alerts.")


def send_alert(site, scenario):
    """

    :return:
    """
    body_message = f"\n\n{site} alert:\n{scenario}."

    client = Client(credentials.SID, credentials.TOKEN)
    [client.messages.create(
        to=number,
        from_=credentials.TRIAL_NUMBER,
        body=body_message,
        status_callback=test_bin,
    ) for number in credentials.call_list]


if __name__ == "__main__":
    sched.start()
