#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module to interract with phpBB forum."""


import re
import time
import sys
from typing import Tuple
from urllib.parse import urljoin
from urllib.error import HTTPError
# from bs4 import BeautifulSoup

from utils.browser import Browser

UCP_URL = 'ucp.php'
LOGIN_MODE = {'mode': 'login'}
LOGOUT_MODE = {'mode': 'logout'}
COOKIE_U_PATTERN = r'phpbb\d?_.*_u'  # new cookie regex
COOKIE_SID_PATTERN = r'phpbb\d?_.*_sid'  # new cookie regex


class PhpBB(object):
    """Class to interract with phpBB forum."""

    FORM_ID = 'postform'
    new_topic_url = 'posting.php?mode=post&f={f}'

    def __init__(self, host):
        """Init object with forum url (host) and Browser object."""
        self.host = host
        try:
            self.browser = Browser()
        except HTTPError as e:
            print(e)
            sys.exit(1)

    def __del__(self):
        """Close the session and delete object."""
        try:
            self.browser.session.close()
        except HTTPError as e:
            print(e)
            sys.exit(1)

    def is_logged(self) -> bool:
        """Check if logged in."""
        u = self._get_user_id()
        if u != 1:
            print(f"login OK : {str(u)}")
            return True
        else:
            print(f"login failed : {str(u)}")
            return False

    def is_logged_out(self) -> bool:
        """Check if logged out."""
        u = self._get_user_id()
        if u != 1:
            print(f"Still logged in : {str(u)}")
            return True
        else:
            print(f"Signed out : {str(u)}")
            return False

    def _get_user_id(self) -> int:
        cookies = self.browser.list_cookies()
        for cookie in cookies:
            if re.search(COOKIE_U_PATTERN, cookie.name):
                return int(cookie.value)

    def _get_sid(self) -> str:
        cookies = self.browser.list_cookies()
        for cookie in cookies:
            if re.search(COOKIE_SID_PATTERN, cookie.name):
                sid = cookie.value
                return sid

    def login(self, username: str, password: str) -> bool:
        """Log in phpBB forum."""
        try:
            forum_ucp = urljoin(self.host, UCP_URL)
            payload = self.browser.select_tag(forum_ucp, "input")
            # for key, value in payload.items():
            #     print(key, value)
            payload['username'] = username
            payload['password'] = password
            time.sleep(1)
            self.browser.post(forum_ucp, params=LOGIN_MODE, data=payload)
            return self.is_logged()

        except HTTPError as e:
            print(e)
            return False

    def logout(self) -> bool:
        """Log out of phpBB forum."""
        try:
            # u_logout = Login(self.browser.session, self.host)
            # u_logout.send_logout()
            forum_ucp = urljoin(self.host, UCP_URL)
            params = {'mode': 'logout', 'sid': self._get_sid()}
            self.browser.post(forum_ucp,
                              # headers=headers,
                              params=params)
            return self.is_logged_out()
        except HTTPError as e:
            print(e)
            return False

    def close(self):
        """Close request session (HTTP connection)."""
        try:
            self.browser.session.close()
        except HTTPError as e:
            print(e)
            sys.exit(1)

    def _make_new_topic_payload(self,
                                url: str,
                                subject: str,
                                desc: str,
                                message: str) -> Tuple[str, dict]:
        form = self.browser.get_form(url, self.FORM_ID)
        form['values']['subject'] = subject
        form['values']['topic_desc'] = desc
        form['values']['message'] = message
        form['values']['post'] = 'Envoyer'
        url = urljoin(self.host, form['action'])
        payload = form['values']
        return url, payload

    def post_topic(self, forum: int, subject: str, desc: str, message: str) -> None:
        """Send a new topic."""
        url = urljoin(self.host, self.new_topic_url.format(f=forum))

        urlsend, payload = self._make_new_topic_payload(url, subject, desc, message)  # noqa: E501
        # print(urlrep)
        # print(payload)
        time.sleep(2)
        self.browser.session.post(urlsend,
                                  # headers=headers,
                                  # params=self.login_mode,
                                  data=payload)
