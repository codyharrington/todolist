__author__ = 'cody'

def handle_default_err_msg(msg, default):
    if msg is None or len(msg.args) == 0:
        return default
    message = msg.args[0]
    if not isinstance(message, str) or len(message) == 0:
        return default
    return message

