try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
    from urllib import urlopen
from pact_test.utils import pact_utils


def test_get_pact_from_url(monkeypatch):
    def fake_website(_):
        return '{"spam": "eggs"}'
    monkeypatch.setattr(pact_utils, 'url_content', fake_website)

    url = 'http://montyphyton.com/'
    url_content = {'spam': 'eggs'}

    assert pact_utils.get_pact_from_url(url) == url_content
