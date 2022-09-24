#!/usr/bin/env python3
import warnings
import os
import sys
import subprocess
import time
import signal
import re
from shutil import which
import threading
warnings.filterwarnings('ignore')

# To Avoid KeyboardInterrupt Error (Not Very Important)
signal.signal(signal.SIGINT, signal.SIG_DFL)

APPINDICATOR_ID = 'express'

used_path = os.path.abspath(os.path.dirname(__file__))
error_image = os.path.join(used_path, 'wrong.png')
working_image = os.path.join(used_path, 'vpn_working.png')


def strip_ansi(text):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]', flags=re.IGNORECASE)
    text = ansi_escape.sub('', text)
    return text


def get_text_needed(text):
    out_lines = []
    for line in text.split("\n"):
        line = line.strip()
        if line and not line.startswith('-') and line not in out_lines:
            out_lines.append(line)
    return '\n'.join(out_lines)


def cli_code():
    """check if app exists."""
    return bool(which("expressvpn"))


def get_status():
    out, error = subprocess.Popen("expressvpn status", shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).communicate()
    out, error = strip_ansi(out.decode().strip()), strip_ansi(error.decode().strip())
    if out:
        return get_text_needed(out+'\n'+error)
    elif cli_code():    # if program exist but returns error
        return get_text_needed(error)
    # if program doesn't exist ..
    # restart service, to keep checking for existence before status (to save checking process & clearer status).
    else:
        os.system("systemctl --user restart startExpressVpn_Monitor.service")
        # close script in case it's not running as a service
        os.kill(os.getpid(), signal.SIGINT)


def app_output():
    return [line.strip().startswith("Connected ") for line in get_status().split('\n')]


def check_display_availability(gui_env_session=['DISPLAY']):
    """
    This function checks if the vars of env that responsible of os gui loaded or not.
    gui_env_session : a list of your chosen env variables keys.
    """
    restart_service = False
    
    for env_key in gui_env_session:
        if not os.environ.get(env_key):
            restart_service = True
            break
    
    if restart_service:
        time.sleep(5)
        subprocess.run(['systemctl', '--user', 'restart', 'startExpressVpn_Monitor'])

# Uncomment the below (check_display_availability) function line : if you want to enable the service -
# without the autostart file while avoiding errors.
# you may change The (check_display_availability) - gui_env_session list,
# * BUT, If you are not sure .. you don't really need to run the function, the service will restart on failure anyway*.

# check_display_availability()
