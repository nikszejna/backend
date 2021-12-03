import re

def extract_videoid(url):
    try:
        id = re.search('^https://.*watch?\?v=(.*)$', url)
        return id.group(1)
    except:
        return  url
