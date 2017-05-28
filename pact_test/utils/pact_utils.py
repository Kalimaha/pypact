import json
try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
    from urllib import urlopen


def get_pact_from_url(url):
    return json.loads(url_content(url))


def url_content(url):
    return urlopen(url).read()
