#!/usr/bin/python3
# -*-coding:utf-8 -*-

"""MDCU."""
import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup



def fetch_mdcu():
    url = "https://www.mdcu-comics.fr/includes/calendrier/inc_calendrier_vf.php"
    dt = datetime.datetime.today()
    params = {'m': dt.month,
              'y': dt.year,
              'format': "01"}
    resp = requests.get(url, params=params)
    soup = BeautifulSoup(resp.text, "html.parser")
    dates = soup.select("h4.m-t-20.m-b-5")

    res = ""

    for d in dates:
        res += d.text + "\n"
        res += "###################################\n"
        issues = d.next_sibling.next_sibling.select("div.p-x-5.m-t-10.text-center > span > h3")  # noqa: E501
        for i in issues:
            if i.a:
                res += f"[url={i.a.get('href')}]{i.text}[/url]\n"
            else:
                res += f"{i.text}\n"
        res += "\n"

    return res
