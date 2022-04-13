import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle


app= Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return render_template('index.html')

app.run(port=5000)