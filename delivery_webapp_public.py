from flask import Flask, request, jsonify, render_template
import h2o
import requests
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np
import urllib.parse

app = Flask(__name__)

# Initialize the H2O server
h2o.init()
# Load your H2O model
model = h2o.load_model("models/h20_automl/DRF_1_AutoML_1_20240505_152221")

# Constants
BING_API_KEY = "key"
WWO_API_KEY = "key"
API_TIMEOUT = 10  # Timeout in seconds for API requests

def get_coordinates(address_query):
    try:
        query = urllib.parse.quote(address_query)
        url = f"http://dev.virtualearth.net/REST/v1/Locations?query={query}&key={BING_API_KEY}&includeEntityTypes=Address"
        response = requests.get(url, timeout=API_TIMEOUT)
        results = response.json()
        if results['resourceSets']:
            resources = results['resourceSets'][0]['resources'][0]
            if 'point' in resources:
                coordinates = resources['point']['coordinates']
                return coordinates
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Error getting coordinates: {e}")
    return None

def determine_hemisphere(country):
    southern_hemisphere = ["Angola", "Argentina", "Australia", "Bolivia", "Botswana", "Brazil",
        "Burundi", "Chile", "Comoros", "DR Congo", "East Timor", "Ecuador",
        "Equatorial Guinea", "Eswatini", "Fiji", "Gabon", "Indonesia", "Kenya",
        "Kiribati", "Lesotho", "Madagascar", "Malawi", "Mauritius", "Mozambique",
        "Namibia", "Nauru", "New Zealand", "Papua New Guinea", "Paraguay", "Peru",
        "Republic of the Congo", "Rwanda", "Samoa", "Sao Tome and Principe",
        "Seychelles", "Solomon Islands", "Somalia", "South Africa", "Tanzania",
        "Tonga", "Tuvalu", "Uganda", "Uruguay", "Vanuatu", "Zambia", "Zimbabwe"]
    return "S" if country in southern_hemisphere else "N"

cycles = {
    'BEG': {'N': ['mar', 'apr', 'may'], 'S': ['sep', 'oct', 'nov']},
    'FFV': {'N': ['jun', 'jul', 'aug', 'sep'], 'S': ['dec', 'jan', 'feb', 'mar']},
    'HED': {'N': ['oct', 'nov', 'dec'], 'S': ['apr', 'may', 'jun']},
    'LD': {'N': ['jan', 'feb'], 'S': ['jul', 'aug']}
}

def get_date_range():
    """Calculate the start and end dates for fetching weather data for the previous year."""
    today = datetime.now()
    
    # Calculate the last day of the previous year
    end_date = today.replace(month=1, day=1) - timedelta(days=1)
    
    # Calculate the start date as one year prior to the end of last year
    start_date = end_date.replace(year=end_date.year - 1)
    
    return start_date, end_date

def fetch_weather_data(lat, lon, start_date, end_date, hemisphere):
    aggregated_data = fetch_weather_for_year(lat, lon, start_date.year, end_date.year)
    
    # Compute averages or sums for each weather type and growth cycle
    weather_data = {}
    for month, months_info in cycles.items():
        for weather_type in ['tmax', 'tmin', 'prcp', 'tavg', 'humidity', 'sunHour']:
            key = f"{weather_type}_{month}"
            values = []
            for month_name in months_info[hemisphere]:
                month_number = month_to_number[month_name.lower()]
                if aggregated_data[month_number][weather_type]:  # Ensure there is data to append
                    values.extend(aggregated_data[month_number][weather_type])  # Use extend for multiple values
            if weather_type in ['tmax', 'tmin']:
                weather_data[key] = np.max(values) if weather_type == 'tmax' else np.min(values) if values else 0
            elif weather_type in ['tavg', 'humidity']:
                weather_data[key] = np.mean(values) if values else 0
            elif weather_type == 'prcp':
                weather_data[key] = np.sum(values)
            elif weather_type == 'sunHour':
                weather_data[key] = np.sum(values)
    
    return weather_data

def fetch_weather_for_year(lat, lon, start_year, end_year):
    aggregated_data = defaultdict(lambda: defaultdict(list))
    
    for year in range(start_year, end_year + 1):
        for month_name, month_number in month_to_number.items():
            data = fetch_weather_for_month(lat, lon, year, month_number)
            for weather_type in ['tmax', 'tmin', 'prcp', 'tavg', 'humidity', 'sunHour']:
                aggregated_data[month_number][weather_type].extend(data[weather_type])

    return aggregated_data

def fetch_weather_for_month(lat, lon, year, month):
    url = f"http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={WWO_API_KEY}&q={lat},{lon}&format=json&date={year}-{month:02d}-01&enddate={year}-{month:02d}-28&tp=24"
    try:
        response = requests.get(url, timeout=API_TIMEOUT)
        if response.status_code == 200:
            month_data = response.json().get('data', {}).get('weather', [])
            daily_data = defaultdict(list)
            for day in month_data:
                daily_data['tmax'].append(float(day.get('maxtempC', 0)))
                daily_data['tmin'].append(float(day.get('mintempC', 0)))
                daily_data['sunHour'].append(float(day.get('sunHour', 0)))
                for hour in day.get('hourly', []):
                    daily_data['tavg'].append(float(hour.get('tempC', 0)))
                    daily_data['prcp'].append(float(hour.get('precipMM', 0)))
                    daily_data['humidity'].append(float(hour.get('humidity', 0)))
            return daily_data
        else:
            print("Failed to retrieve data:", response.status_code)
    except requests.RequestException as e:
        print("Request failed:", e)
    return defaultdict(list)

month_to_number = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
}

@app.route('/')
def home():
    # Render the HTML form at the root.
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        address = request.form['address']
        coordinates = get_coordinates(address)
        if not coordinates:
            return jsonify({'error': 'Address not found'})

        country = request.form.get('country', '')
        
        # Define hemisphere based on the country
        hemisphere = determine_hemisphere(country)
        
        start_date, end_date = get_date_range()
        
        # Extract latitude and longitude from coordinates
        lat, lon = coordinates
        
        weather_data = fetch_weather_data(lat, lon, start_date, end_date, hemisphere)

        # Prepare data for H2O model prediction
        df = h2o.H2OFrame(weather_data)
        predictions = model.predict(df).as_data_frame()

        return jsonify(predictions.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)