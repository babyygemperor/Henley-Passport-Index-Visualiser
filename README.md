# Visa Requirements Map

This project is a Flask web application hosted on https://passports.aamin.dev that visualises the visa requirements for each country. It allows you to select a country and see the visa requirements for that country. The requirements are displayed on a world map and also in a list. The visa requirements are shown using colour-coded regions on the world map: blue for the selected country, green for visa-free countries, yellow for countries requiring an eVisa, red for countries requiring a visa, and grey for countries for which there is no data.

## Getting Started

### Prerequisites

- Python 3.8 or later
- Flask 1.1.2 or later
- pandas 1.1.5 or later
- numpy 1.19.5 or later
- folium 0.12.1 or later
- Jinja2 2.11.3 or later

### Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/babyygemperor/Henley-Passport-Index-Visualiser.git
```

2. Navigate into the project directory:

```bash
cd Henley-Passport-Index-Visualiser
```

3. Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

Run the application using the command:

```bash
python main.py
```

The application will start a server that you can access through your browser at `localhost:5000`.

## Structure of the Application

- `main.py`: The main Python script that handles the data processing and runs the server.
- `visa_requirements.csv`: The csv file that contains the visa requirements data.
- `visa_free_statistics.csv`: The csv file that contains the visa-free score for each country.
- `world.geojson`: The GeoJSON data that contains the geographical boundaries of each country.
- `templates/index.html`: The main HTML file that renders the web page.
- `static/styles.css`: The CSS file that styles the web page.
- `static/flags`: The directory containing the flag images for each country.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to [OpenStreetMap](https://www.openstreetmap.org/) for the base maps.
- Thanks to [flagcdn](https://flagcdn.com/) for the flag icons.
