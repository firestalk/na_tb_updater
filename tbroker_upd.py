#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
import os
import sys
import logging
from time import sleep
# Set current dirrectory to file path
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
# Logging
logging.basicConfig(level=logging.INFO, filename='status.log', format='%(asctime)s - %(message)s', datefmt='%m-%d %H:%M:%S')
log = logging.getLogger('tb_updater')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%m-%d %H:%M:%S')
ch.setFormatter(formatter)
log.addHandler(ch)

PAUSE = 600
LOGIN = 'YOURLOGIN@MAIL.ADDR'
PASS = 'YOURPASSWORD'
IFC_P = 'https://ifconfigme.herokuapp.com/'  # Fast clone of ifconfig.me
IFC_S = 'http://ifconfig.me/ip'  # Second chance


def main():
    our_ip = get_ip()
    resp = set_ip(our_ip)
    if 'FAIL!' in resp and 'already registered' not in resp:
        log.warn("Update Failed")
        log.warn("Response: {}".format(resp))
    elif 'OK!' in resp:
        log.info("Successfully updated IP")
    else:
        log.info("Seems like IP intact")
    sys.exit(0)


def set_ip(our_ip):
    try:
        upd = requests.get('https://tb.netassist.ua/autochangeip.php?l={}&p={}&ip={}'.format(LOGIN, PASS, our_ip))
    except ConnectionError:
        log.warn("Connection Error. Sleeping {} sec and retrying...".format(PAUSE))
        sleep(PAUSE)
        return set_ip(our_ip)
    if upd.status_code != 200:
        log.warn("Update Failed.")
        log.warn("Status Code: {}, Response: {}".format(upd.status_code, upd.text))
    return upd.text


def get_ip():
    try:
        req = requests.get(IFC_P)
    except ConnectionError:
        log.warn("Connection Error. Sleeping {} sec and retrying...".format(PAUSE))
        sleep(PAUSE)
        return get_ip()
    if req.status_code != 200:
        log.info("Primary IP check failed.")
        try:
            req = requests.get(IFC_S)
        except ConnectionError:
            log.warn("Connection Error. Sleeping {} sec and retrying...".format(PAUSE))
            sleep(PAUSE)
            return get_ip()
    if req.status_code != 200:
        log.info("Failed to determine our IP")
        sys.exit(1)
    else:
        log.info('IP: {}'.format(req.text))
    return req.text


if __name__ == '__main__':
    main()
