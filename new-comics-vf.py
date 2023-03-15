#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""Docstring."""

import logging
import os
from datetime import date

from dotenv import load_dotenv

from utils.mdcu import fetch_mdcu
from utils.phpbb import PhpBB

logging.basicConfig(level=logging.INFO)

# Parse a .env file and then load all the variables found as environment variables.  # noqa: E501
load_dotenv()

HOST = os.getenv("HOST")
USERNAME = os.getenv("NAME")
PASSWORD = os.getenv("PASSWORD")

content = fetch_mdcu()
phpbb = PhpBB(HOST)

if phpbb.login(USERNAME, PASSWORD):
    today = date.today()
    subject = today.strftime(f'Sorties du mois {today.month}/{today.year} (VF)')  # noqa: E501
    desc = ""
    phpbb.post_topic(7, subject, desc, content)
    phpbb.logout()
    phpbb.close()
