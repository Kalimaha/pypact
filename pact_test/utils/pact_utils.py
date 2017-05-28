import json
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen


def get_pact(location):
    if location.startswith(('http', 'https')):
        return __get_pact_from_url(location)
    return __get_pact_from_file(location)


def __get_pact_from_file(filename):
    with open(filename) as file_content:
        return json.loads(file_content.read())


def __get_pact_from_url(url):
    return json.loads(__url_content(url))


def __url_content(url):         # pragma: no cover
    return urlopen(url).read()  # pragma: no cover
