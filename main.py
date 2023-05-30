import numpy
from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS, cross_origin
import pandas as pd
import folium
import json
from folium import MacroElement
from jinja2 import Template

app = Flask(__name__, static_folder='static')
CORS(app, origins=['http://127.0.0.1:5000', 'http://localhost:5000'])

# Load the visa requirements data
df = pd.read_csv('visa_requirements.csv')
score_df = pd.read_csv('visa_free_statistics.csv')
# Load data
countries = df['Origin'].unique().tolist()


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow requests from any origin
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'  # Allow POST and OPTIONS methods
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Allow 'Content-Type' header
    return response


def get_visa_free_score(country):
    return score_df[(score_df['Origin'] == country)]['Visa Free'].values[0]


def get_country_requirement_list(country):
    return df[df['Origin'] == country].drop('Origin', axis=1).rename(
        columns={"Destination": "country", "Requirement": "status", 'Destination Code': 'country_A3'}) \
        .replace({numpy.nan: country}).to_dict('records')


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')


@app.route('/countries', methods=['POST', 'GET'])
def get_country_list():
    return jsonify(countries)


@app.route('/country', methods=['POST'])
def get_country_details():
    print(request.json)
    return jsonify(get_country_requirement_list(request.json.get('country')))


@app.route('/score', methods=['POST'])
def get_country_score():
    return str(get_visa_free_score(request.json.get('country')))


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
