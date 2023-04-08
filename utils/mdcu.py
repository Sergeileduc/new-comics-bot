#!/usr/bin/python3
# -*-coding:utf-8 -*-

"""MDCU."""
import datetime

import requests
from bs4 import BeautifulSoup


def fetch_issue(url: str) -> str:
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.select_one("div.widget-item > h4")
        return title.text
    except Exception:
        return None


def issue2string(issue) -> str:
    if not issue.a:
        return f"{issue.text}\n"
    title = fetch_issue(issue.a.get('href'))
    return f"[url={issue.a.get('href')}]{title}[/url]\n" if title else f"[url={issue.a.get('href')}]{issue.text}[/url]\n"  # noqa: E501


def fetch_mdcu():
    url = "https://www.mdcu-comics.fr/includes/calendrier/inc_calendrier_vf.php"  # noqa: E501
    dt = datetime.datetime.now()
    params = {'m': dt.month,
              'y': dt.year,
              'format': "01"}
    resp = requests.get(url, params=params)
    soup = BeautifulSoup(resp.text, "html.parser")
    dates = soup.select("h4.m-t-20.m-b-5")

    res = ""

    for d in dates:
        res += d.text + "\n"
        res += "--------------------------------------\n"
        issues = d.next_sibling.next_sibling.select("div.p-x-5.m-t-10.text-center > span > h3")  # noqa: E501
        for i in issues:
            res += issue2string(i)
        res += "\n"

    return res
