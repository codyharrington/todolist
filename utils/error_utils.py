__author__ = 'cody'

def handle_default_err_msg(msg, default):
    if msg == "" or not isinstance(msg, str):
        return default
    return msg

