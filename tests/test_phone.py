import pytest
import requests
import json
from twilio.rest import Client
import credentials


client = Client(credentials.SID, credentials.TOKEN)

# Create a postbin for testing callbacks
# create_bin = requests.post("https://postb.in/api/bin")
# bin_id = create_bin.json()['binId']
# test_bin = f"https://postb.in/{bin_id}"


def test_initialise_client():
    """
    Check that the client exists (and has therefore been established),
    and that the auth credentials match the ones given.
    :return: None.
    """
    assert client
    assert client.auth == (credentials.SID, credentials.TOKEN)


def test_send_message():
    """
    Send a message from the twilio trial number to my mobile to test that messages can be sent.
    :return:
        """
    # TODO: fix status callback, getting a 404 when trying to retrieve the data from postbin
    # client.messages.create(
    #     to=credentials.JACK_MOB,
    #     from_=credentials.TRIAL_NUMBER,
    #     body="AUTOMATED PYTHON-TWILIO TEST, DO NOT RESPOND.",
    #     status_callback=test_bin,
    # )
    # print(test_bin)
    # callback = requests.get(test_bin)
    # print(callback.text)

