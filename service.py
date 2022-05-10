from flask import Flask, request
from web_scraper import Parser

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/classification")
def news_classification():
    """
    Given article URL, extract article text, predict if article is "true" or "false"
    :return: Article prediction along with confidence score
    """
    article_url = user = request.args.get('url')
    return "Hello, Salvador"


@app.route("/correction")
def user_correction():
    article_url = user = request.args.get('url')
    return "Hello, Salvador"


if __name__ == "__main__":
    app.run(debug=True)
