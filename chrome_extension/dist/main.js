const confidence = document.querySelector("#confidence");
const prediction = document.querySelector("#prediction");
const domain = document.querySelector("#domain");
const credibility = document.querySelector("#credibility");
const hits = document.querySelector("#hits");
const suggest = document.querySelector("#suggest");
const preds = document.querySelector("#preds");
const loaoder = document.querySelector("#loader");
const undefined_div = document.querySelector("#undefined");
window.onload = function () {
    preds.style.display = 'none';
    loaoder.style.display = 'block';
    undefined_div.style.display = 'none';
    chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
        let url = tabs[0].url;
        fetch('http://localhost:5000/classification?url=' + url)
            .then((res) => res.json())
            .then((res) => {
                loaoder.style.display = 'none';
                if (res.status == "OK") {
                    preds.style.display = 'block';
                    confidence.innerHTML = (parseFloat(res.confidence_score) * 100).toPrecision(2).toString() + '%';
                    prediction.innerHTML = res.predicted_label.toString();
                    if (res.predicted_label)
                        prediction.style.color = 'green';
                    else
                        prediction.style.color = 'red';
                    domain.innerHTML = res.website_domain;
                    credibility.innerHTML = ((res.website_true / res.website_hits) * 100).toPrecision(2);
                    hits.innerHTML = res.website_hits;
                    suggest.innerHTML = "Report as " + (!res.predicted_label).toString();

                    document.getElementById("suggest").addEventListener("click", suggest_change);
                    function suggest_change() {
                        fetch('http://localhost:5000/correction?url=' + url + '&userlabel=' + (+(!res.predicted_label)).toString());
                    }
                }
                else {
                    undefined_div.style.display = 'block';
                }
            });
    });
}