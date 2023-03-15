#!/usr/bin/python3
# -*-coding:utf-8 -*-

"""League of comics API."""
import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# publisher 1 is DC
# publisher 2 is Marvel
# indie comics are all comics, excluding 1 and 2 (the Big Two)


def fetch_issues(publisher=None,
                 week=False,
                 m=None, y=None,
                 firsts_only=False):
    """Fetch new comics on leagueofcomics.

    Keyword Arguments:
        publisher {str} -- Publisher : DC or Marvel or Indie or None (All) (default: {None})
        week {bool} -- Week or Month mode (default: {False})
        m {int} -- month (default: {None})
        y {int} -- year (default: {None})
        firsts_only {bool} -- #1 only ? (default: {False})

    Returns:
        list -- list of comics formated as :
        {"title": <title>,
         "cover": <cover url>,
         "url": <league of comics url>}

    Examples:
        issues = fetch_issues()
        issues = fetch_issues(publisher="DC", week=True, firsts_only=True)
        issues = fetch_issues(publisher="Marvel", firsts_only=True, m=2, y=2020)
    """  # noqa: E501
    loc_url = "https://leagueofcomicgeeks.com"
    api_url = "https://leagueofcomicgeeks.com/comic/get_comics"

    params = {"addons": 1,
              "list": "releases",
              "date_type": "previews",
              "date": None,
              "date_end": None,
              "user_id": 0,
              "view": "list",
              "format[]": [1, 6],  # Regular issues + Annuals ??
              "publisher_exclude[]": [],
              "publisher[]": [],
              "list_refinement": None,
              #   "order": "alpha-asc"  # or by popularity : "order": "pulls"
              }

    # Select by publisher DC / Marvel / Indie
    if publisher == "DC":
        params["publisher[]"] = 1
    elif publisher == "Marvel":
        params["publisher[]"] = 2
    elif publisher == "Indie":
        params["publisher_exclude[]"] = [1, 2]

    today = datetime.date.today()

    # Current week
    if week:
        params["date_type"] = "week"
        params["date"] = today.strftime("%m/%d/%Y")
    # User month and year
    elif m and y:
        params["date"] = f"{m}/01/{y}"
    # Current month
    else:
        params["date"] = today.strftime("%m/01/%Y")

    # Only first issues ?
    if firsts_only:
        params["list_refinement"] = "firsts"

    # fetch league of comics
    resp = requests.get(api_url, params=params)
    # Parse response
    json_ = resp.json()['list']
    soup = BeautifulSoup(json_, "html.parser")
    # raw_list = soup.select("li.media")  # old CSS selector
    raw_list = soup.select('#comic-list-issues > li')
    # each element of raw_list is a comic html html div
    # with cover, title, synopsis, date, price, etc...

    # We make a list of comics dictionnary like :
    # {"title": <title>,
    #  "cover": <cover url>,
    #   "url": <league of comics url>}
    comics = [{"title": r.select_one('div.title.color-primary > a').text,
               "publisher": r.select_one('div.comic-details > span.publisher').text,  # noqa: E501
               "cover": r.find("div", class_="comic-cover-art").img['data-src'],  # noqa: E501
               "url": urljoin(loc_url, r.select_one("div.title > a")["href"])}  # noqa: E501
              for r in raw_list]

    return comics


def print_issue(issue):
    """Pretty prints a "comic" dictionnary."""
    print('\t' + issue["title"])
    print('\t' + issue["cover"].split("?")[0])
    print('\t' + issue["url"])
    print()


def generate_forum_list(publisher=None):
    issues = fetch_issues(publisher=publisher, week=True)
    issues.sort(key=lambda item: item.get("title"))
    issues.sort(key=lambda item: item.get("publisher"))

    res = "".join(
        f"{i.get('publisher'):30} -> [url={i.get('url')}]{i.get('title')}[/url]\n"  # noqa : E501
        if publisher == "Indie"
        else f"[url={i.get('url')}]{i.get('title')}[/url]\n"
        for i in issues
    )
    return res
