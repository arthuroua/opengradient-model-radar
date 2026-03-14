from flask import Flask, request
import requests

app = Flask(__name__)

MODEL_API = "https://hub.opengradient.ai/api/models"

def get_models():
    try:
        r = requests.get(MODEL_API, timeout=10)
        data = r.json()
        models = data.get("models", [])
        return models
    except:
        return []

def search_models(query, models):
    results = []
    q = query.lower()

    for m in models:
        name = m.get("name","").lower()
        desc = m.get("description","").lower()

        if q in name or q in desc:
            results.append(m)

    return results[:5]


@app.route("/", methods=["GET","POST"])
def home():

    models = get_models()

    trending = sorted(models, key=lambda x: x.get("downloads",0), reverse=True)[:6]
    newest = sorted(models, key=lambda x: x.get("created_at",""), reverse=True)[:6]

    answer_html = ""

    if request.method == "POST":

        query = request.form.get("query","")
        results = search_models(query, models)

        if results:
            answer_html += "<h3>Results:</h3>"
            for r in results:
                name = r.get("name","Unknown")
                desc = r.get("description","No description")

                answer_html += f"""
                <div class='assistant-card'>
                <b>{name}</b><br>
                {desc}
                </div>
                """
        else:
            answer_html = "<p>No models found.</p>"


    def render_cards(data):
        html=""
        for m in data:
            name = m.get("name","Unknown")
            desc = m.get("description","No description")

            html+=f"""
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

<title>OpenGradient Radar</title>

<style>

body {{
margin:0;
font-family:Arial;
background:#070b14;
color:white;
}}

.header {{
padding:40px;
text-align:center;
}}

.title {{
font-size:42px;
font-weight:bold;
background:linear-gradient(90deg,#00E5FF,#7B61FF);
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
margin-top:40px;
}}

.section-title {{
color:#00E5FF;
margin-bottom:20px;
font-size:22px;
}}

.grid {{
display:grid;
grid-template-columns:repeat(auto-fill,minmax(250px,1fr));
gap:20px;
}}

.card {{
background:#111827;
padding:20px;
border-radius:12px;
border:1px solid #1f2937;
transition:0.2s;
}}

.card:hover {{
border:1px solid #00E5FF;
transform:translateY(-4px);
}}

.model-name {{
font-size:18px;
font-weight:bold;
margin-bottom:6px;
}}

.model-desc {{
opacity:0.7;
font-size:14px;
}}

.assistant-box {{
background:#111827;
padding:25px;
border-radius:12px;
border:1px solid #1f2937;
}}

input {{
width:70%;
padding:12px;
border-radius:8px;
border:none;
background:#1f2937;
color:white;
}}

button {{
padding:12px 20px;
border:none;
background:#00E5FF;
color:black;
border-radius:8px;
cursor:pointer;
margin-left:10px;
}}

button:hover {{
background:#7B61FF;
color:white;
}}

.assistant-card {{
background:#1f2937;
padding:15px;
border-radius:8px;
margin-top:10px;
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

<div class="title">OpenGradient Radar</div>
<div class="subtitle">Explore and search models from the OpenGradient Model Hub</div>

</div>

<div class="container">

<div class="section">

<div class="section-title">🤖 AI Model Assistant</div>

<div class="assistant-box">

<form method="POST">

<input name="query" placeholder="Ask something like: crypto prediction model">
<button>Search</button>

</form>

{answer_html}

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
