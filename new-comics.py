#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""Docstring."""


import logging
import os
from datetime import date

from dotenv import load_dotenv

from utils.leagueofcomics import generate_forum_list
from utils.phpbb import PhpBB

logging.basicConfig(level=logging.INFO)

# Parse a .env file and then load all the variables found as environment variables.  # noqa: E501
load_dotenv()

HOST = os.getenv("HOST")
USERNAME = os.getenv("NAME")
PASSWORD = os.getenv("PASSWORD")

dc_list = generate_forum_list(publisher="DC")
marvel_list = generate_forum_list(publisher="Marvel")
indie_list = generate_forum_list(publisher="Indie")

forum_list = "" + "[size=150]DC COMICS[/size]\n"
forum_list += dc_list
forum_list += "\n\n"
forum_list += "[size=150]Marvel COMICS[/size]\n"
forum_list += marvel_list
forum_list += "\n\n"
forum_list += "[size=150]Indie COMICS[/size]\n"
forum_list += indie_list
forum_list += "\n\n"


phpbb = PhpBB(HOST)

if phpbb.login(USERNAME, PASSWORD):
    today = date.today()
    subject = today.strftime('Semaine du %d/%m/%Y (VO)')
    desc = ""

    phpbb.post_topic(139, subject, desc, forum_list)

    phpbb.logout()
    phpbb.close()
