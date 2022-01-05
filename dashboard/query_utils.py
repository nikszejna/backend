import re


def extract_videoid(url):
    """Returns youtube video id from url, assumes is a url or standalone video id"""
    try:
        id = re.search("^https://.*watch?\?v=(.*)$", url)
        return id.group(1)
    except:
        return url
