"""Module for functions to be used in flask app."""
import os           # for getenv
from datetime import datetime   # for reformatting json date and inserting day of the week
import requests     # for html requests
from dotenv import load_dotenv  # to load api_key from .env file together with os.getenv()
import custom_exceptions       # for self defined exceptions
import custom_classes   # for self defined api error messages

load_dotenv()
API_KEY = os.getenv('API_KEY')
# edit these global vars to change the daytime and nighttime values (0-23)
DAYTIME_HOUR = 7
NIGHTTIME_HOUR = 19


def send_request(location):
    """function accessed visual crossing api and retrieves the requested weather data"""
    target_api = (f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/'
                  f'timeline/{location}?unitGroup=metric&key={API_KEY}&contentType=json')
    # response code for the get request
    try:
        response = requests.get(target_api, timeout=30)
        if response.status_code != 200:
            raise \
            custom_exceptions.DataError(response.status_code,
                                        custom_classes.ErrorDict.str_dict[response.status_code])
    except requests.exceptions.Timeout:
        return "Error, timed out"
    # parse and send json data
    return parse_json_data(response.json())


def parse_json_data(weather_json):
    """function goes over json data and extracts only required data"""
    # get first 7 days, there are 15 total
    weather_data_list = [weather_json["resolvedAddress"]]
    # loop to iterate over all
    for day in weather_json['days'][:DAYTIME_HOUR]:
        day_data = {}
        # parse date from api to time_object
        day_date_object = datetime.strptime(day['datetime'], '%Y-%m-%d').date()
        # convert time_object into weekday string and re-format the date
        day_data['day'] = day_date_object.strftime('%A')
        day_data['date'] = day_date_object.strftime('%d-%m-%Y')
        day_data['day_icon'] = day['hours'][DAYTIME_HOUR]['icon']
        day_data['day_temp'] = day['hours'][DAYTIME_HOUR]['temp']
        day_data['night_temp'] = day['hours'][NIGHTTIME_HOUR]['temp']
        day_data['humidity'] = day['humidity']
        weather_data_list.append(day_data)
    return weather_data_list
