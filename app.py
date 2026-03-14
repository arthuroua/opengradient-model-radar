from flask import Flask, request
import requests
import random

app = Flask(__name__)

MODEL_API = "https://hub.opengradient.ai/api/models"


def get_models():
    try:
        r = requests.get(MODEL_API, timeout=10)
        data = r.json()
        return data.get("models", [])
    except:
        return []


def trending_models(models):
    return sorted(models, key=lambda x: x.get("downloads", 0), reverse=True)[:8]


@app.route("/", methods=["GET", "POST"])
def home():

    models = get_models()
    trending = trending_models(models)

    insight = ""

    if request.method == "POST":
        question = request.form.get("question","").lower()

        if "trending" in question:
            insight = "🔥 Trending models right now:<br>"
            for m in trending[:5]:
                insight += f"• {m.get('name','Unknown')}<br>"

        elif "recommend" in question:
            insight = "🧠 Recommended models:<br>"
            picks = random.sample(trending, min(3,len(trending)))
            for m in picks:
                insight += f"• {m.get('name','Unknown')}<br>"

        else:
            insight = "Try asking: <i>trending models</i> or <i>recommend models</i>"


    cards=""

    for m in trending:

        name = m.get("name","Unknown")
        desc = m.get("description","No description")

        score = random.randint(70,98)

        cards += f"""
        <div class="card">

        <div class="model-name">{name}</div>

        <div class="model-desc">{desc}</div>

        <div class="score">Trending Score: {score}</div>

        </div>
        """


    html=f"""

<html>

<head>

<title>OpenGradient Insights</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

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
font-size:48px;
font-weight:bold;
background:linear-gradient(90deg,#00f2ff,#8a5cff);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}}

.subtitle{{
opacity:0.6;
}}

.container{{
max-width:1200px;
margin:auto;
padding:20px;
}}

.grid{{
display:grid;
grid-template-columns:repeat(auto-fill,minmax(250px,1fr));
gap:20px;
}}

.card{{
background:#0f1424;
border-radius:12px;
padding:20px;
border:1px solid #1c233a;
transition:0.2s;
}}

.card:hover{{
transform:translateY(-5px);
border:1px solid #00f2ff;
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

.ai-box{{
background:#0f1424;
border-radius:12px;
padding:25px;
border:1px solid #1c233a;
}}

input{{
width:70%;
padding:12px;
border-radius:8px;
border:none;
background:#1c233a;
color:white;
}}

button{{
padding:12px 20px;
margin-left:10px;
background:#00f2ff;
border:none;
border-radius:8px;
cursor:pointer;
}}

button:hover{{
background:#8a5cff;
color:white;
}}

.section{{
margin-top:50px;
}}

.section-title{{
color:#00f2ff;
font-size:22px;
margin-bottom:20px;
}}

.chart-box{{
background:#0f1424;
padding:20px;
border-radius:12px;
border:1px solid #1c233a;
}}

</style>

</head>

<body>

<div class="header">

<div class="title">OpenGradient Insights</div>

<div class="subtitle">AI analytics for the Model Hub</div>

</div>


<div class="container">


<div class="section">

<div class="section-title">🤖 AI Model Analyst</div>

<div class="ai-box">

<form method="POST">

<input name="question" placeholder="Ask: trending models or recommend models">

<button>Analyze</button>

</form>

<p>{insight}</p>

</div>

</div>



<div class="section">

<div class="section-title">🔥 Trending Models</div>

<div class="grid">

{cards}

</div>

</div>



<div class="section">

<div class="section-title">📈 Model Hub Activity</div>

<div class="chart-box">

<canvas id="chart"></canvas>

</div>

</div>


</div>



<script>

const ctx=document.getElementById('chart');

new Chart(ctx,{{
type:'line',

data:{{

labels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],

datasets:[{{

label:'Model Activity',

data:[12,19,14,22,30,28,35],

borderColor:'#00f2ff',

tension:0.4

}}]

}}

}})

</script>


</body>

</html>

"""

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
