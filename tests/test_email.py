import imaplib
import yaml

# Import credentials from config file
with open('config.yaml', 'r') as config_file:
    config = yaml.load(config_file)

mail_credentials = config["generators gmail"]


def test_read_inbox():
    """

    :return:
    """
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(mail_credentials["username"], mail_credentials["password"])
    mail.select('Inbox')
    stringers_type, stringers_data = mail.search(None, '(FROM "stringershydro@hallidays.com" UNSEEN)')

    assert stringers_type == "OK"

