from flask import Flask, render_template
import requests

app = Flask(__name__)

MODEL_API = "https://hub.opengradient.ai/api/models"

@app.route("/")
def home():
    try:
        r = requests.get(MODEL_API)
        data = r.json()

        models = data.get("models", [])

        trending = sorted(models, key=lambda x: x.get("downloads", 0), reverse=True)[:5]
        newest = sorted(models, key=lambda x: x.get("created_at", ""), reverse=True)[:5]

    except:
        trending = []
        newest = []

    return render_template("index.html", trending=trending, newest=newest)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
