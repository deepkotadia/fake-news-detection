from urllib.parse import urlparse


def parse_url_string(url):
    parsed_url = urlparse(url)
    website_domain, url_path = parsed_url.netloc, parsed_url.path
    return website_domain, url_path
