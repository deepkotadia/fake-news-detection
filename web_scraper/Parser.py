from bs4 import BeautifulSoup
import requests

HTML_PARSER = 'html.parser'
def send_get_requests(url):
    r = requests.get(url)
    return r.text

def extract_npr_paragraph(soup):
    map = []
    for x in soup.findAll('main'):
        for y in soup.findAll('p'):
            string_arr = y.text.split()
            if(len(string_arr) > 5):
                map.append(" ".join(string_arr))
    map = map[1:]
    print(map)
    return map

def extract_apnews_paragraph(soup):
    print(soup.head.title.text)
    map = []
    for x in soup.find_all("div", class_="Article"):
        for y in x.findAll('p'):
            string_arr = y.text.split()
            map.append(" ".join(string_arr))
    print(map)
    return map

def extract_bluntforcetruth_para(soup):
    map = []
    for x in soup.find_all("div", class_="text-description"):
        for y in x.findAll('p'):
            string_arr = y.text.split()
            map.append(" ".join(string_arr))
    print(map)
    return map

def extract_express_co_uk_para(soup):
    map = []
    for x in soup.find_all("div", class_="text-description"):
        for y in x.findAll('p'):
            string_arr = y.text.split()
            map.append(" ".join(string_arr))
    print(map)
    return map


def extract_general_para(soup):
    map = []
    for x in soup.findAll("p"):
        string_arr = x.text.split()
        map.append(" ".join(string_arr))
    print(f"the complete data is \n{map}")


def get_content_from_scraper(url):
    # url = "https://www.npr.org/2022/04/26/1061867530/kamala-harris-test-positive-covid-vice-president"
    # url = https://apnews.com/article/capitol-siege-biden-presidential-elections-electoral-college-mark-meadows-296ddf04ffaacec07f548a2a997af448
    html = send_get_requests(url)
    # print(f"the html content is {html}")
    soup = BeautifulSoup(html, HTML_PARSER)
    result = None
    if "www.npr.org" in url:
        result = extract_npr_paragraph(soup)
    elif "apnews.com" in url:
        result = extract_apnews_paragraph(soup)
    elif "www.express.co.uk" in url:
        result = extract_express_co_uk_para(soup)
    elif "www.thetimes.co.uk" in url or "www.snopes.com" in url:
        result = extract_general_para(soup)
    elif len(result) == 0:
        result = extract_general_para(soup)


    return " ".join(result)

# FAKE ARTICLES
# https://bluntforcetruth.com/news/huge-scandal-oregon-changes-hundreds-of-republican-ballots-to-non-partisan-denying-gop-voters-the-right-to-participate-in-primary/
# https://www.snopes.com/fact-check/did-schiff-visit-epsteins-island/
# https://100percentfedup.com/this-is-amazing-in-1984-the-new-york-times-said-trump-would-be-our-best-president-they-forgot/
# https://www.express.co.uk/life-style/health/1405891/coronavirus-vaccine-side-effects-arthralgia-joint-pain-pfzier-jab

text = get_content_from_scraper("https://www.express.co.uk/life-style/health/1405891/coronavirus-vaccine-side-effects-arthralgia-joint-pain-pfzier-jab")
print(text)
# parsing_content("https://www.thetimes.co.uk/article/keir-starmers-instant-decision-on-resignation-took-three-days-to-be-revealed-kjf9bkp5k")
# parsing_content("https://apnews.com/article/capitol-siege-biden-presidential-elections-electoral-college-mark-meadows-296ddf04ffaacec07f548a2a997af448")
# html = send_get_requests("https://www.npr.org/sections/health-shots/2022/04/26/1094881056/older-adults-shouldnt-start-a-routine-of-daily-aspirin-task-force-says")
# html = send_get_requests("https://www.npr.org/2022/04/26/1061867530/kamala-harris-test-positive-covid-vice-president")
# soup = BeautifulSoup(html, 'html.parser')
# extract_the_npr_paragraph(soup)
## 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