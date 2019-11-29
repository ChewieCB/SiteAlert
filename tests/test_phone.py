from twilio.rest import Client
import json
import yaml
import requests

# Import credentials from config file
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

twilio_credentials = config["twilio"]
personal_numbers = config["personal numbers"]

# Initialise the twilio client
test_client = Client(twilio_credentials["TEST_SID"], twilio_credentials["TEST_TOKEN"])
client = Client(twilio_credentials["SID"], twilio_credentials["TOKEN"])

# Create a postbin for testing callbacks
create_bin = requests.post("https://postb.in/api/bin")
bin_id = json.loads(create_bin.text)['binId']
test_bin = f"https://postb.in/api/bin/{bin_id}"


def test_initialise_client():
    """
    Check that the client exists (and has therefore been established),
    and that the auth credentials match the ones given.
    :return: None.
    """
    assert test_client
    assert client
    assert test_client.auth == (twilio_credentials["TEST_SID"], twilio_credentials["TEST_TOKEN"])
    assert client.auth == (twilio_credentials["SID"], twilio_credentials["TOKEN"])


def test_send_message():
    """
    Send a message from the twilio trial number to my mobile to test that messages can be sent.
    :return:
        """
    # TODO: fix status callback, getting a 404 when trying to retrieve the data from postbin
    test_message = test_client.messages.create(
        to="+15005550006",
        from_=twilio_credentials["TEST_NUMBER"],
        body="AUTOMATED PYTHON-TWILIO TEST, DO NOT RESPOND.",
        status_callback=test_bin,
    )
    print(test_bin)
    callback = requests.get(test_bin)
    print(callback.text)
    requests.delete(test_bin)

