from flask import Flask, request, jsonify
from datetime import datetime
import pandas as pd
from ml_model import test
import utils
from web_scraper.parser import NewsWebsiteScraper

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/classification")
def news_classification():
    """
    Given article URL, extract article text, predict if article is "true" or "false"
    :return: Article prediction along with confidence score
    Example Request: http://127.0.0.1:5000/classification?url=https://www.npr.org/2022/05/09/1096617152/a-warhol-marilyn-brings-a-record-auction-price-195-million
    """
    article_url = request.args.get("url")

    # Scrape article text from URL
    news_website_scraper = NewsWebsiteScraper()
    article_scraped_text = news_website_scraper.get_content_from_scraper(url=article_url)

    # The scraper/parser supports only some websites currently, check if this news website is supported
    threshold = 20
    content_found = False
    if len(article_scraped_text) > threshold:
        content_found = True
    if not content_found:
        return jsonify({"status": "Website not Supported"})

    # Process URL string
    website_domain, url_path = utils.parse_url_string(article_url)

    # Predict if article is true or false with confidence score
    pred, prob = test.infer_model(article_scraped_text)
    pred_label, conf_score = False if pred == "false" else True, float(prob)

    # Add model prediction details to model_predictions table
    model_predictions_df = pd.read_csv(filepath_or_buffer="data/model_predictions.csv")
    update_ts = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    new_row_df = pd.DataFrame([{
        "timestamp": update_ts,
        "full_url": article_url,
        "website_domain": website_domain,
        "url_path": url_path,
        "article_text": article_scraped_text,
        "label": pred_label,
        "confidence_score": conf_score
    }])
    updated_model_predictions_df = pd.concat([model_predictions_df, new_row_df], ignore_index=True)
    updated_model_predictions_df.to_csv("data/model_predictions.csv", index=False)

    # Compute website credibility score from model_predictions and user_corrections tables
    user_corrections_df = pd.read_csv(filepath_or_buffer="data/user_corrections.csv")
    cols = ["website_domain", "label"]
    combined_df = pd.concat([updated_model_predictions_df[cols], user_corrections_df[cols]], ignore_index=True)
    website_domain_df = combined_df[combined_df["website_domain"] == website_domain]
    total_hits = website_domain_df.shape[0]
    total_true = website_domain_df[website_domain_df["label"] == True].shape[0]

    # Build and return response (classification, confidence) back to front-end
    response = jsonify({"status": "OK",
                        "predicted_label": pred_label, "confidence_score": conf_score,
                        "website_domain": website_domain, "website_hits": total_hits, "website_true": total_true})
    return response


@app.route("/correction")
def user_correction():
    """
    Given article URL and user label (1 for True, 0 for False) for it, add it to user correction table
    :return: Update timestamp if successful
    Example Request: http://127.0.0.1:5000/correction?url=https://www.npr.org/2022/05/09/1096617152/a-warhol-marilyn-brings-a-record-auction-price-195-million&userlabel=0
    """

    article_url = request.args.get("url")
    user_classification = request.args.get("userlabel")
    label = bool(int(user_classification))

    # Scrape article text from URL
    news_website_scraper = NewsWebsiteScraper()
    article_scraped_text = news_website_scraper.get_content_from_scraper(url=article_url)

    # The scraper/parser supports only some websites currently, check if this news website is supported
    threshold = 20
    content_found = False
    if len(article_scraped_text) > threshold:
        content_found = True
    if not content_found:
        return jsonify({"status": "Website not Supported"})

    # Process URL string
    website_domain, url_path = utils.parse_url_string(article_url)

    # Add user feedback record to user_corrections table
    user_corrections_df = pd.read_csv(filepath_or_buffer="data/user_corrections.csv")
    update_ts = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    new_row_df = pd.DataFrame([{
        "timestamp": update_ts,
        "full_url": article_url,
        "website_domain": website_domain,
        "url_path": url_path,
        "article_text": article_scraped_text,
        "label": label
    }])
    updated_user_corrections_df = pd.concat([user_corrections_df, new_row_df], ignore_index=True)
    updated_user_corrections_df.to_csv("data/user_corrections.csv", index=False)

    response = jsonify({"status": "OK", "feedback_update_ts": update_ts})
    return response


if __name__ == "__main__":
    app.run(debug=True)
