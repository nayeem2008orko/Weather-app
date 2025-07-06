import requests
from django.shortcuts import render
from datetime import datetime

def index(request):
    current_weather = None
    forecast_data = []
    background_class = "default"
    error = None

    if request.method == 'POST':
        city = request.POST.get('city')
        from django.conf import settings
        api_key = settings.OPENWEATHER_API_KEY


        # Get current weather
        current_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'

        current_response = requests.get(current_url)
        forecast_response = requests.get(forecast_url)

        if current_response.status_code == 200 and forecast_response.status_code == 200:
            current_data = current_response.json()
            forecast_json = forecast_response.json()

            condition = current_data['weather'][0]['main'].lower()
            if 'cloud' in condition:
                background_class = 'clouds'
            elif 'rain' in condition:
                background_class = 'rain'
            elif 'clear' in condition:
                background_class = 'clear'
            elif 'snow' in condition:
                background_class = 'snow'
            else:
                background_class = 'default'

            current_weather = {
                'city': city,
                'temperature': current_data['main']['temp'],
                'description': current_data['weather'][0]['description'].title(),
                'icon': current_data['weather'][0]['icon'],
            }

            # Extract one forecast per day (at 12:00)
            for entry in forecast_json['list']:
                if '12:00:00' in entry['dt_txt']:
                    forecast_data.append({
                        'date': datetime.strptime(entry['dt_txt'], "%Y-%m-%d %H:%M:%S").strftime("%a, %b %d"),
                        'temp': entry['main']['temp'],
                        'desc': entry['weather'][0]['description'].title(),
                        'icon': entry['weather'][0]['icon'],
                    })
        else:
            error = "City not found. Please try again."

    context = {
        'current_weather': current_weather,
        'forecast_data': forecast_data,
        'background_class': background_class,
        'error': error,
    }
    return render(request, 'weather_app/index.html', context)
