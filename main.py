from flask import Flask, render_template, request
import pandas as pd
import folium
import json
from folium import MacroElement
from jinja2 import Template

app = Flask(__name__, static_folder='static')

# Load the visa requirements data
df = pd.read_csv('visa_requirements.csv')
# Load data
countries = df['Origin'].unique().tolist()


@app.route('/', methods=['GET', 'POST'])
def index():
    show_map = False
    if request.method == 'POST':
        show_map = True
        country = request.form.get('select_country')
        m = create_map(country)
        m.save('static/map.html')
    return render_template('index.html', countries=countries, show_map=show_map, selected_country=country)


class NoWrapTiles(MacroElement):
    def __init__(self):
        super(NoWrapTiles, self).__init__()
        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    noWrap: true,
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                }).addTo({{ this._parent.get_name() }});
            {% endmacro %}
            """)


def create_map(country):
    data = df[df['Origin'] == country]
    # Initialise the map:
    m = folium.Map(location=[0, 0], zoom_start=2, min_zoom=2)
    m.add_child(NoWrapTiles())

    # Load the GeoJSON data
    with open('world.geojson') as f:
        geojson_data = json.load(f)

    # Transform non-numeric Requirement to numeric codes
    mapping = {'N/A': 0, 'Visa Free': 1, 'eVisa': 2, 'Visa Required': 3}
    data = data.fillna(value=0)
    data['Requirement'] = data['Requirement'].replace(mapping)
    data['Requirement'] = data['Requirement'].astype(int)

    # Create a colour dictionary
    colour_dict = {0: 'blue', 1: 'green', 2: 'yellow', 3: 'red'}

    # Add the GeoJSON layer
    folium.GeoJson(
        geojson_data,
        name='choropleth',
        style_function=lambda feature: {
            'fillColor': colour_dict[
                data[data['Destination Code'] == feature['properties']['ISO_A3']]['Requirement'].values[0]]
            if not data[data['Destination Code'] == feature['properties']['ISO_A3']].empty else 'grey',
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.7,
            'lineOpacity': 0.2,
        }
    ).add_to(m)

    folium.LayerControl().add_to(m)

    return m


if __name__ == '__main__':
    app.run(debug=True)


def find_visa_required_countries(country):
    df_local = df[(df['Origin'] == country) & (df['Requirement'] == 'Visa Required')]
    return df_local['Destination'].values.tolist()


def find_visa_free_countries(country):
    df_local = df[(df['Origin'] == country) & (df['Requirement'] != 'Visa Required')]
    return df_local['Destination'].values.tolist()
