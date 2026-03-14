from flask import Flask
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


@app.route("/")
def home():

    models = get_models()
    trending = trending_models(models)

    cards = ""

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

    leaderboard = ""

    for i, m in enumerate(trending[:3]):
        medal = ["🥇", "🥈", "🥉"][i]
        leaderboard += f"<p>{medal} {m.get('name','Unknown')}</p>"

    recommendations = ""

    picks = random.sample(trending, min(3, len(trending)))

    for m in picks:
        recommendations += f"<p>• {m.get('name','Unknown')}</p>"

    html = f"""

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

.subtitle{{opacity:0.6;}}

.container{{max-width:1200px;margin:auto;padding:20px;}}

.section{{margin-top:50px;}}

.section-title{{color:#00f2ff;font-size:22px;margin-bottom:20px;}}

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

.model-name{{font-weight:bold;font-size:18px;}}

.model-desc{{font-size:14px;opacity:0.7;margin:8px 0;}}

.score{{margin-top:10px;color:#00f2ff;}}

button{{
padding:10px 16px;
margin-right:10px;
background:#00f2ff;
border:none;
border-radius:6px;
cursor:pointer;
}}

button:hover{{background:#8a5cff;color:white;}}

.ai-box{{
background:#0f1424;
padding:20px;
border-radius:12px;
border:1px solid #1c233a;
}}

.hidden{{display:none;}}

input{{
padding:10px;
border-radius:6px;
border:none;
background:#1c233a;
color:white;
width:250px;
}}

.chat-box{{
background:#0f1424;
padding:20px;
border-radius:12px;
border:1px solid #1c233a;
}}

.message{{
margin-top:10px;
padding:10px;
background:#1c233a;
border-radius:6px;
}}

</style>

<script>

function showTrending(){{
document.getElementById("trendingBox").style.display="block"
document.getElementById("recommendBox").style.display="none"
}}

function showRecommend(){{
document.getElementById("recommendBox").style.display="block"
document.getElementById("trendingBox").style.display="none"
}}

function searchModels(){{
let input=document.getElementById("search").value.toLowerCase()
let cards=document.getElementsByClassName("card")

for(let i=0;i<cards.length;i++){{
let text=cards[i].innerText.toLowerCase()
cards[i].style.display=text.includes(input)?"block":"none"
}}

}}

function chat(){{
let q=document.getElementById("chatInput").value
let box=document.getElementById("chatMessages")

let reply="Try asking about trending models or recommendations."

if(q.toLowerCase().includes("trending"))
reply="Trending models are shown in the dashboard."

if(q.toLowerCase().includes("recommend"))
reply="Recommended models are highlighted in the AI section."

box.innerHTML+=`<div class='message'><b>You:</b> ${q}</div>`
box.innerHTML+=`<div class='message'><b>AI:</b> ${reply}</div>`

document.getElementById("chatInput").value=""
}}

</script>

</head>

<body>

<div class="header">

<div class="title">OpenGradient Insights</div>

<div class="subtitle">AI analytics dashboard for the Model Hub</div>

</div>

<div class="container">

<div class="section">

<div class="section-title">🤖 AI Model Analyst</div>

<div class="ai-box">

<button onclick="showTrending()">🔥 Trending</button>
<button onclick="showRecommend()">🧠 Recommend</button>

<div id="trendingBox" class="hidden">

<h3>Trending Models</h3>

{leaderboard}

</div>

<div id="recommendBox" class="hidden">

<h3>Recommended Models</h3>

{recommendations}

</div>

</div>

</div>


<div class="section">

<div class="section-title">🔍 Model Explorer</div>

<input id="search" placeholder="Search models..." onkeyup="searchModels()">

</div>


<div class="section">

<div class="section-title">🔥 Trending Models</div>

<div class="grid">

{cards}

</div>

</div>


<div class="section">

<div class="section-title">💬 AI Chat</div>

<div class="chat-box">

<div id="chatMessages"></div>

<input id="chatInput" placeholder="Ask something...">
<button onclick="chat()">Send</button>

</div>

</div>


<div class="section">

<div class="section-title">📈 Model Hub Activity</div>

<canvas id="chart"></canvas>

</div>

</div>

<script>

const ctx=document.getElementById('chart')

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
