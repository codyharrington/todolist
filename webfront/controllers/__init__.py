__author__ = 'cody'
from webfront import failed_ip_login_attempt_counts, app

def increment_failed_logins(ip):
    if ip not in failed_ip_login_attempt_counts:
        failed_ip_login_attempt_counts[ip] = 1
    else:
        failed_ip_login_attempt_counts[ip] += 1

def clear_failed_logins(ip):
    if ip in failed_ip_login_attempt_counts:
        del failed_ip_login_attempt_counts[ip]
        app.logger.warning("{} failed login count has been cleared".format(ip))

def ip_failed_previously(ip):
    return ip in failed_ip_login_attempt_counts

def ip_attempts_past_threshold(ip):
    if ip not in failed_ip_login_attempt_counts:
        return False
    return failed_ip_login_attempt_counts[ip] >= app.config["FAILED_ATTEMPTS_CAPTCHA_THRESHOLD"]

def set_ip_to_threshold(ip):
    failed_ip_login_attempt_counts[ip] = app.config["FAILED_ATTEMPTS_CAPTCHA_THRESHOLD"]

def should_display_captcha(ip, forced_captcha=False):
    if app.config["DISABLE_ALL_RECAPTCHA"]:
        return False
    if forced_captcha:
        return app.config["FORCED_RECAPTCHA_ENABLED"]
    if ip_attempts_past_threshold(ip) and app.config["REACTIVE_RECAPTCHA_ENABLED"]:
        app.logger.warning("{} is past the failed login threshold".format(ip))
        return True
    return False
