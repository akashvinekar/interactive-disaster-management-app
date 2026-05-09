from flask import Flask, render_template
import folium
from folium.plugins import MiniMap
import json
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Load location data
with open('data/locations.json', 'r') as file:
    data = json.load(file)

@app.route('/')
def home():

    # Create map
    disaster_map = folium.Map(
        location=[13.6288, 79.4192],
        zoom_start=12
    )

    # Add hospitals
    for hospital in data['hospitals']:
        folium.Marker(
            [hospital['lat'], hospital['lon']],
            popup=hospital['name'],
            icon=folium.Icon(color='red')
        ).add_to(disaster_map)

    # Add shelters
    for shelter in data['shelters']:
        folium.Marker(
            [shelter['lat'], shelter['lon']],
            popup=shelter['name'],
            icon=folium.Icon(color='green')
        ).add_to(disaster_map)

    # Add safe zones
    for zone in data['safe_zones']:
        folium.Marker(
            [zone['lat'], zone['lon']],
            popup=zone['name'],
            icon=folium.Icon(color='blue')
        ).add_to(disaster_map)
    # Danger Zones

    folium.Circle(
        location=[13.6288, 79.4192],
        radius=3000,
        color='red',
        fill=True,
        fill_color='red',
        popup='Flood Risk Zone'
    ).add_to(disaster_map)

    folium.Circle(
        location=[13.6500, 79.4300],
        radius=2000,
        color='orange',
        fill=True,
        fill_color='orange',
        popup='Medium Risk Area'
    ).add_to(disaster_map)
    # Mini Map

    minimap = MiniMap()

    disaster_map.add_child(minimap)
        # Weather API

    api_key =os.getenv("WEATHER_API_KEY")

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q=Tirupati&appid={api_key}"

    try:

        response = requests.get(weather_url)

        weather_data = response.json()

        weather = weather_data['weather'][0]['description']

        temp = weather_data['main']['temp'] - 273.15

        popup_text = f"Weather: {weather} | Temp: {temp:.1f}°C"

        folium.Marker(
            [13.6288, 79.4192],
            popup=popup_text,
            icon=folium.Icon(color='purple')
        ).add_to(disaster_map)

    except:
        print("Weather API Error")
    # Convert map to HTML
    map_html = disaster_map._repr_html_()

    return render_template(
        'index.html',
        map_html=map_html
    )

if __name__ == '__main__':
    app.run(debug=True)