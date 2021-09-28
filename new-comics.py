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

DC_list = generate_forum_list(publisher="DC")
Marvel_list = generate_forum_list(publisher="Marvel")
Indie_list = generate_forum_list(publisher="Indie")

forum_list = ""
forum_list += "[size=150]DC COMICS[/size]\n"
forum_list += DC_list
forum_list += "\n\n"
forum_list += "[size=150]Marvel COMICS[/size]\n"
forum_list += Marvel_list
forum_list += "\n\n"
forum_list += "[size=150]Indie COMICS[/size]\n"
forum_list += Indie_list
forum_list += "\n\n"


phpbb = PhpBB(HOST)

if phpbb.login(USERNAME, PASSWORD):
    today = date.today()
    subject = today.strftime('Semaine du %d/%m/%Y')
    desc = ""
    
    phpbb.post_topic(139, subject, desc, forum_list)
    
    phpbb.logout()
    phpbb.close()
