from flask import Flask
import requests
import random

app = Flask(__name__)

MODEL_API = "https://hub.opengradient.ai/api/models"


def get_models():
    try:
        r = requests.get(MODEL_API, timeout=10)

        if r.status_code != 200:
            return []

        data = r.json()

        if isinstance(data, dict):
            return data.get("models", [])

        return []

    except Exception as e:
        print("API error:", e)
        return []


def trending_models(models):

    if not models:
        return []

    return sorted(models, key=lambda x: x.get("downloads", 0), reverse=True)[:8]


@app.route("/")
def home():

    models = get_models()
    trending = trending_models(models)

    cards = ""

    if not trending:
        cards = "<p>No models available right now.</p>"

    else:
        for m in trending:

            name = m.get("name", "Unknown")
            desc = m.get("description", "No description")

            score = random.randint(70, 98)

            cards += f"""
            <div class="card">
            <div class="model-name">{name}</div>
            <div class="model-desc">{desc}</div>
            <div class="score">Trending Score: {score}</div>
            </div>
            """

    html = f"""

    <html>

    <head>

    <title>OpenGradient Insights</title>

    <style>

    body{{
    background:#05070d;
    color:white;
    font-family:Arial;
    margin:0;
    }}

    .header{{
    text-align:center;
    padding:50px;
    }}

    .title{{
    font-size:42px;
    font-weight:bold;
    background:linear-gradient(90deg,#00f2ff,#8a5cff);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    }}

    .grid{{
    max-width:1000px;
    margin:auto;
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(250px,1fr));
    gap:20px;
    }}

    .card{{
    background:#0f1424;
    border-radius:12px;
    padding:20px;
    border:1px solid #1c233a;
    }}

    .model-name{{
    font-weight:bold;
    font-size:18px;
    }}

    .model-desc{{
    font-size:14px;
    opacity:0.7;
    margin:8px 0;
    }}

    .score{{
    margin-top:10px;
    color:#00f2ff;
    }}

    </style>

    </head>

    <body>

    <div class="header">

    <div class="title">OpenGradient Insights</div>

    </div>

    <div class="grid">

    {cards}

    </div>

    </body>

    </html>

    """

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
