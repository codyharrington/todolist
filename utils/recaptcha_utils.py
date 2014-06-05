__author__ = 'cody'
from utils.request_utils import *
from utils.messages import recaptcha_messages
import requests

def check_recaptcha(private_key, verification_url):
    c_challenge = form_data("c_challenge")
    c_response = form_data("c_response")
    ip = request.remote_addr

    data = {
        "privatekey": private_key,
        "remoteip": ip,
        "challenge": c_challenge,
        "response": c_response
    }

    response = requests.post(verification_url, data)
    values = response.text.split("\n")

    return values[0], recaptcha_messages(values[1])

