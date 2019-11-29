import sys
import imaplib
import email

import yaml
from twilio.rest import Client
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

test_bin = ""     # TODO: add a bin for status response data when its working

active_site_list = [
    ("Stringers", "stringershydro@hallidays.com"),
    ("Osbaston", "relay+1932-0069-24@relay.talk2m.com"),
]


@sched.scheduled_job('interval', minutes=1)
def main():
    """
    Run the get_inbox function with the active_site_list arg.
    :return:
    """
    get_inbox(active_site_list)


def get_inbox(site_emails: list):
    """
    :param site_emails: list of tuples containing two strings, the name and email address of a site.
    :return:
    """
    # Get mail credentials from config file
    mail_credentials = config["generators gmail"]
    # Get gmail server and login
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(mail_credentials["username"], mail_credentials["password"])
    mail.select('Inbox')
    # Assign site email data to a dict
    site_data = {
        site[0]: (mail.search(None, f'(FROM "{site[1]}" UNSEEN)')) for site in site_emails}
    #     "Stringers": (mail.search(None, '(FROM "stringershydro@hallidays.com" UNSEEN)')),
    #     "Osbaston": (mail.search(None, '(FROM "relay+1932-0069-24@relay.talk2m.com" UNSEEN)')),
    # }
    # stringers_type, stringers_data = mail.search(None, '(FROM "stringershydro@hallidays.com" UNSEEN)')
    # ostbaston_type, osbaston_data = mail.search(None, '(FROM "relay+1932-0069-24@relay.talk2m.com" UNSEEN)')

    # Assign a dict with a key/value pair of each given site and and empty list to be filled with alerts
    unseen_scenarios = {site: [] for site in site_data.keys()}
    # Get the subject of every unseen email in the inbox from one of the target emails
    for site, data in site_data.items():
        for num in data[1][0].split():
            typ, data = mail.fetch(num, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1].decode('utf-8'))
                    scenario = msg['subject'].split(site)[1]
                    unseen_scenarios[site].append(scenario)
    # Check each site for unseen emails, send a text to the call list if any are found
    for site in unseen_scenarios.keys():
        sys.stdout.write(f"\n\nSite: {site}")
        if unseen_scenarios[site]:
            # [send_alert(site, scenario) for site, scenario in unseen_scenarios.items()]
            sys.stdout.write(f"\n\t{len(unseen_scenarios[site])} alerts sent.")
            [sys.stdout.write(f"\n\tAlert: {scenario}") for scenario in unseen_scenarios[site]]
        else:
            sys.stdout.write("\n\tNo unseen alerts.")


def send_alert(site, scenario):
    """

    :return:
    """
    # Get twilio and phone credentials
    twilio_credentials = config["twilio"]
    personal_numbers = config["personal numbers"]
    # Get a list of numbers to alert
    call_list = personal_numbers.values()
    # Build the test message
    body_message = f"\n\n{site} alert:\n{scenario}."
    # Connect to the twilio client
    client = Client(twilio_credentials["SID"], twilio_credentials["TOKEN"])
    # Send a text message with the alerts to each number on the call list
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
