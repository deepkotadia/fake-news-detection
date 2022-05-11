from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

from enum import Enum


class NEWS_WEBSITES(Enum):
    NPR = "www.npr.org"
    APNEWS = "apnews.com"
    EXPRESS_CO_UK = "www.express.co.uk"
    TIMES_CO_Uk = "www.thetimes.co.uk"
    SNOPES = "www.snopes.com"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

class NewsWebsiteScraper():

    def __init__(self):
        self.websites = NEWS_WEBSITES
        self.HTML_PARSER = 'html.parser'

    def get_hostname_from_url(self, url):
        parsed_url = urlparse(url)
        return parsed_url.hostname

    def is_website_supported(self, url):
        hostname = self.get_hostname_from_url(url)
        return self.websites.has_value(hostname)

    def send_get_requests(self, url):
        r = requests.get(url)
        return r.text

    def extract_npr_paragraph(self, soup):
        map = []
        for x in soup.findAll('main'):
            for y in soup.findAll('p'):
                string_arr = y.text.split()
                if(len(string_arr) > 5):
                    map.append(" ".join(string_arr))
        map = map[1:]
        return map

    def extract_apnews_paragraph(self, soup):
        map = []
        for x in soup.find_all("div", class_="Article"):
            for y in x.findAll('p'):
                string_arr = y.text.split()
                map.append(" ".join(string_arr))
        return map

    def extract_bluntforcetruth_para(self, soup):
        map = []
        for x in soup.find_all("div", class_="text-description"):
            for y in x.findAll('p'):
                string_arr = y.text.split()
                map.append(" ".join(string_arr))
        return map

    def extract_express_co_uk_para(self, soup):
        map = []
        for x in soup.find_all("div", class_="text-description"):
            for y in x.findAll('p'):
                string_arr = y.text.split()
                map.append(" ".join(string_arr))
        return map


    def extract_general_para(self, soup):
        map = []
        for x in soup.findAll("p"):
            string_arr = x.text.split()
            map.append(" ".join(string_arr))
        return map


    def get_content_from_scraper(self, url):

        html = self.send_get_requests(url)
        soup = BeautifulSoup(html, self.HTML_PARSER)
        hostname = self.get_hostname_from_url(url)
        result = None
        if self.websites.NPR.value in hostname:
            result = self.extract_npr_paragraph(soup)
        elif self.websites.APNEWS.value in hostname:
            result = self.extract_apnews_paragraph(soup)
        elif self.websites.EXPRESS_CO_UK.value in hostname:
            result = self.extract_express_co_uk_para(soup)
        else:
            result = self.extract_general_para(soup)
        if result is None or len(result) == 0:
            result = self.extract_general_para(soup)
        if result is not None and len(result) > 0:
            return " ".join(result)
        else:
            return ""


# FAKE ARTICLES
# https://bluntforcetruth.com/news/huge-scandal-oregon-changes-hundreds-of-republican-ballots-to-non-partisan-denying-gop-voters-the-right-to-participate-in-primary/
# https://www.snopes.com/fact-check/did-schiff-visit-epsteins-island/
# https://100percentfedup.com/this-is-amazing-in-1984-the-new-york-times-said-trump-would-be-our-best-president-they-forgot/
# https://www.express.co.uk/life-style/health/1405891/coronavirus-vaccine-side-effects-arthralgia-joint-pain-pfzier-jab

text = NewsWebsiteScraper().get_content_from_scraper("https://apnews.com/article/capitol-siege-biden-presidential-elections-electoral-college-mark-meadows-296ddf04ffaacec07f548a2a997af448")
# print(text)
# url = "https://www.npr.org/2022/04/26/1061867530/kamala-harris-test-positive-covid-vice-president"
# url = https://apnews.com/article/capitol-siege-biden-presidential-elections-electoral-college-mark-meadows-296ddf04ffaacec07f548a2a997af448
# parsing_content("https://www.thetimes.co.uk/article/keir-starmers-instant-decision-on-resignation-took-three-days-to-be-revealed-kjf9bkp5k")
# parsing_content("https://apnews.com/article/capitol-siege-biden-presidential-elections-electoral-college-mark-meadows-296ddf04ffaacec07f548a2a997af448")
# html = send_get_requests("https://www.npr.org/sections/health-shots/2022/04/26/1094881056/older-adults-shouldnt-start-a-routine-of-daily-aspirin-task-force-says")
# html = send_get_requests("https://www.npr.org/2022/04/26/1061867530/kamala-harris-test-positive-covid-vice-president")
## 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