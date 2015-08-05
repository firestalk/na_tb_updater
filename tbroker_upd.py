#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
import os
import sys
import logging
# Set current dirrectory to file path
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
# Logging
logging.basicConfig(level=logging.INFO, filename='status.log', format='%(asctime)s - %(message)s', datefmt='%m-%d %H:%M:%S')
log = logging.getLogger('tb_updater')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%m-%d %H:%M:%S')
ch.setFormatter(formatter)
log.addHandler(ch)

LOGIN = 'YOURLOGIN@MAIL.ADDR'
PASS = 'YOURPASSWORD'
IFC_P = 'https://ifconfigme.herokuapp.com/'  # Fast clone of ifconfig.me
IFC_S = 'http://ifconfig.me/ip'  # Second chance


def main():
    req = requests.get(IFC_P)
    if req.status_code != 200:
        log.info("Primary IP check failed.")
        req = requests.get(IFC_S)
    if req.status_code != 200:
        log.info("Failed to determine our IP")
        sys.exit(1)
    else:
        log.info('IP: {}'.format(req.text))
    upd = requests.get('https://tb.netassist.ua/autochangeip.php?l={}&p={}&ip={}'.format(LOGIN, PASS, req.text))
    if upd.status_code != 200:
        log.warn("Update Failed.")
        log.warn("Status Code: {}, Response: {}".format(upd.status_code, upd.text))
    resp = upd.text
    if 'FAIL!' in resp and 'already registered' not in resp:
        log.warn("Update Failed")
        log.warn("Response: {}".format(resp))
    elif 'OK!' in resp:
        log.info("Successfully updated IP")
    else:
        log.info("Seems like IP intact")
    sys.exit(0)


if __name__ == '__main__':
    main()
