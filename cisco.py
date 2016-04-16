#!/usr/bin/env python
from selenium import webdriver
import itertools
import time


DRIVER = webdriver.Firefox()
DRIVER.implicitly_wait(2)
CISCO_ROUTER_URL = 'https://172.16.1.1/default.htm'
DRIVER.get("https://172.16.1.1/default.htm")
SWITCH_INTERVAL = 20


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


def main():
    page_login()
    switch_to_frame('menuPage')
    menu = DRIVER.find_element_by_id('menuNode_4')
    menu.click()
    mn = DRIVER.find_element_by_id('MNL41')
    mn.click()
    switch_to_frame('contentFrame')
    for text in itertools.cycle(['WAN1', 'WAN2']):
        print('Switching to %s...' % text)
        lkw = DRIVER.find_element_by_name('SmartLKW')
        select_lkw(lkw, text)
        save_lkw()
        time.sleep(SWITCH_INTERVAL)

main()
