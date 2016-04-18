#!/usr/bin/env python
from selenium import webdriver
import itertools
import os
import sys
import time


DRIVER = None
CISCO_ROUTER_URL = 'https://172.16.1.1/default.htm'
SWITCH_INTERVAL = int(os.environ.get('SWITCH_INTERVAL', 40))


def parse_args():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.isdigit():
            if arg in ['1', '2']:
                return 'WAN' + arg
            else:
                raise Exception('invalid WAN number')
        else:
            if arg in ['WAN1', 'WAN2']:
                return arg
            else:
                raise Exception('invalid WAN name')
    else:
        return False


def load_driver():
    global DRIVER
    DRIVER = webdriver.Firefox()
    DRIVER.get("https://172.16.1.1/default.htm")
    DRIVER.implicitly_wait(2)


def read_secret():
    with open('.secret') as f:
        return f.read().strip()


def page_login():
    username = DRIVER.find_element_by_name("username")
    username.send_keys('cisco')
    password = DRIVER.find_element_by_name("password")
    password.send_keys(read_secret())
    login = DRIVER.find_element_by_id('Login')
    login.click()
    DRIVER.get(CISCO_ROUTER_URL)


def switch_to_frame(frame_id):
    DRIVER.switch_to_default_content()
    DRIVER.switch_to_frame(DRIVER.find_element_by_id(frame_id))


def select_lkw(lkw, text):
    for option in lkw.find_elements_by_tag_name('option'):
        if option.text == text:
            option.click()
            break


def save_lkw():
    save = DRIVER.find_element_by_id('Save')
    save.click()


def switch_wan(wan):
    lkw = DRIVER.find_element_by_name('SmartLKW')
    select_lkw(lkw, wan)
    save_lkw()
    print('Switched to %s' % wan)


def alternate():
    for text in itertools.cycle(['WAN1', 'WAN2']):
        switch_wan(text)
        time.sleep(SWITCH_INTERVAL)


def main():
    wan = parse_args()
    load_driver()
    page_login()
    switch_to_frame('menuPage')
    menu = DRIVER.find_element_by_id('menuNode_4')
    menu.click()
    mn = DRIVER.find_element_by_id('MNL41')
    mn.click()
    switch_to_frame('contentFrame')
    if wan is False:
        alternate()
    else:
        switch_wan(wan)
    DRIVER.close()


if __name__ == '__main__':
    main()
