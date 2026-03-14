from flask import Flask
import random

app = Flask(__name__)

models = [
"ETH Volatility Predictor",
"Crypto Sentiment AI",
"Market Regime Detector",
"BTC Price Predictor",
"DeFi Risk Analyzer",
"AI Trading Agent",
"Portfolio Optimizer",
"Onchain Data Analyzer",
"Liquidity Predictor",
"Gas Fee Estimator"
]

signals = [
"Bullish",
"Bearish",
"High Volatility",
"Positive Sentiment",
"Risk Increase"
]

@app.route("/")
def home():

    cards=""

    for m in models:

        confidence=random.randint(60,95)
        signal=random.choice(signals)

        size=confidence*2

        color="#16c784" if confidence>80 else "#f3ba2f" if confidence>70 else "#ea3943"

        cards+=f"""

        <div class="tile" style="width:{size}px;height:{size}px;background:{color};">

        <div class="tile-title">{m}</div>

        <div class="tile-signal">{signal}</div>

        <div class="tile-score">{confidence}%</div>

        </div>

        """

    html=f"""

<html>

<head>

<title>OpenGradient AI Heatmap</title>

<style>

body{{
background:#05070d;
color:white;
font-family:Arial;
margin:0;
}}

.header{{
text-align:center;
padding:40px;
}}

.title{{
font-size:44px;
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

.heatmap{{
display:flex;
flex-wrap:wrap;
gap:10px;
justify-content:center;
}}

.tile{{
border-radius:10px;
display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
text-align:center;
font-size:12px;
padding:10px;
transition:0.2s;
cursor:pointer;
}}

.tile:hover{{
transform:scale(1.1);
}}

.tile-title{{
font-weight:bold;
margin-bottom:4px;
}}

.tile-signal{{
opacity:0.8;
}}

.tile-score{{
font-size:16px;
font-weight:bold;
margin-top:4px;
}}

.legend{{
display:flex;
justify-content:center;
gap:20px;
margin-top:20px;
}}

.legend div{{
display:flex;
align-items:center;
gap:6px;
}}

.box{{
width:14px;
height:14px;
border-radius:3px;
}}

.green{{background:#16c784}}
.yellow{{background:#f3ba2f}}
.red{{background:#ea3943}}

</style>

</head>

<body>

<div class="header">

<div class="title">OpenGradient AI Heatmap</div>

<div class="subtitle">AI Model Market Signals</div>

</div>

<div class="container">

<div class="heatmap">

{cards}

</div>

<div class="legend">

<div><div class="box green"></div> Strong</div>

<div><div class="box yellow"></div> Neutral</div>

<div><div class="box red"></div> Weak</div>

</div>

</div>

</body>

</html>

"""

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
