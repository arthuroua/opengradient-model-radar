from flask import Flask, request
import requests

app = Flask(__name__)

MODEL_API = "https://hub.opengradient.ai/api/models"


def get_models():
    try:
        r = requests.get(MODEL_API, timeout=10)
        data = r.json()
        return data.get("models", [])
    except:
        return []


def analyze_models(models):

    trending = sorted(models, key=lambda x: x.get("downloads", 0), reverse=True)[:6]
    newest = sorted(models, key=lambda x: x.get("created_at", ""), reverse=True)[:6]

    return trending, newest


@app.route("/", methods=["GET", "POST"])
def home():

    models = get_models()
    trending, newest = analyze_models(models)

    insight = ""

    if request.method == "POST":
        question = request.form.get("question", "").lower()

        if "trending" in question:
            insight = "<b>Trending models right now:</b><br>"
            for m in trending[:3]:
                insight += f"• {m.get('name','Unknown')}<br>"

        elif "new" in question:
            insight = "<b>Newest models:</b><br>"
            for m in newest[:3]:
                insight += f"• {m.get('name','Unknown')}<br>"

        else:
            insight = "Try asking: <i>trending models</i> or <i>new models</i>"

    def render_cards(data):
        html = ""
        for m in data:
            name = m.get("name", "Unknown Model")
            desc = m.get("description", "No description")

            html += f"""
            <div class="card">
                <div class="model-name">{name}</div>
                <div class="model-desc">{desc}</div>
            </div>
            """
        return html

    html = f"""
<!DOCTYPE html>
<html>
<head>

<title>Model Insights AI</title>

<style>

body {{
margin:0;
font-family:Arial;
background:#05070d;
color:white;
}}

.header {{
text-align:center;
padding:50px;
}}

.title {{
font-size:48px;
font-weight:bold;
background:linear-gradient(90deg,#00f2ff,#8a5cff);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}}

.subtitle {{
opacity:0.6;
}}

.container {{
max-width:1200px;
margin:auto;
padding:20px;
}}

.section {{
margin-top:50px;
}}

.section-title {{
font-size:22px;
color:#00f2ff;
margin-bottom:20px;
}}

.grid {{
display:grid;
grid-template-columns:repeat(auto-fill,minmax(260px,1fr));
gap:20px;
}}

.card {{
background:#0f1424;
border:1px solid #1c233a;
border-radius:12px;
padding:20px;
transition:0.25s;
}}

.card:hover {{
transform:translateY(-5px);
border:1px solid #00f2ff;
}}

.model-name {{
font-size:18px;
font-weight:bold;
margin-bottom:6px;
}}

.model-desc {{
font-size:14px;
opacity:0.7;
}}

.ai-box {{
background:#0f1424;
border-radius:12px;
padding:25px;
border:1px solid #1c233a;
}}

input {{
width:70%;
padding:12px;
border-radius:8px;
border:none;
background:#1c233a;
color:white;
}}

button {{
padding:12px 20px;
margin-left:10px;
background:#00f2ff;
border:none;
border-radius:8px;
cursor:pointer;
}}

button:hover {{
background:#8a5cff;
color:white;
}}

.insight {{
margin-top:15px;
opacity:0.9;
}}

.footer {{
text-align:center;
margin-top:60px;
opacity:0.4;
}}

</style>

</head>

<body>

<div class="header">

<div class="title">Model Insights AI</div>
<div class="subtitle">Analytics dashboard for the OpenGradient Model Hub</div>

</div>


<div class="container">

<div class="section">

<div class="section-title">🤖 AI Model Analyst</div>

<div class="ai-box">

<form method="POST">

<input name="question" placeholder="Ask: trending models or new models">
<button>Analyze</button>

</form>

<div class="insight">
{insight}
</div>

</div>

</div>


<div class="section">

<div class="section-title">🔥 Trending Models</div>

<div class="grid">

{render_cards(trending)}

</div>

</div>


<div class="section">

<div class="section-title">🆕 New Models</div>

<div class="grid">

{render_cards(newest)}

</div>

</div>


<div class="footer">

Built for the OpenGradient community

</div>

</div>

</body>
</html>
"""

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
