#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Module to handle HTTP requests (with requests lib)."""

import requests
from urllib.error import HTTPError
from bs4 import BeautifulSoup


class Browser:
    """Class to make HTTP requests."""

    def __init__(self):
        """Init Browser with a requests.Session()."""
        try:
            self.session = requests.Session()
        except HTTPError as e:
            raise e

    def get_html(self, url: str) -> BeautifulSoup:
        """Return HTML soup with Beautiful Soup.

        Args:
            url (str): url

        Returns:
            soup: HMTL soup

        """
        # headers = {}
        # headers['User-Agent'] = self.user_agent
        try:
            r = self.session.get(url)
            return BeautifulSoup(r.text, "html.parser")
        except HTTPError as e:
            print("HTTP Error")
            print(e)

    def get_form(self, url: str, form_id):
        """Return form found in url as a dict."""
        try:
            form = self.get_html(url).find("form", id=form_id)
            return self._get_form_values(form)
        except HTTPError as e:
            print(e)
            raise

    @staticmethod
    def _get_form_values(soup):
        try:
            inputs = soup.find_all("input")
            values = {
                inp["name"]: inp["value"]
                for inp in inputs
                if inp.get("type") != "submit"
                and inp.get("name")
                and inp.get("value")
            }
            return {"values": values, "action": soup["action"]}
        except AttributeError as e:
            print(f"Attribute Error : {str(e)}")
        except KeyError as e:
            print(f"Key Error code : {str(e)}")

    def select_tag(self, url, tag):
        """Select tag in soup and return dict (name:value)."""
        soup = self.get_html(url)
        items = soup.select(tag)
        return {i['name']: i['value'] for i in items if i.has_attr('value')}

    def post(self, url, **kwargs):
        """Send POST request using requests."""
        return self.session.post(url, **kwargs)

    def list_cookies(self):
        """List session cookies."""
        return list(self.session.cookies)
