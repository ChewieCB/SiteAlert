import imaplib
import credentials


def test_read_inbox():
    """

    :return:
    """
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(credentials.gen_user, credentials.gen_pass)
    mail.select('Inbox')
    stringers_type, stringers_data = mail.search(None, '(FROM "stringershydro@hallidays.com" UNSEEN)')

    assert stringers_type == "OK"

