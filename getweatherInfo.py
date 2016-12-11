#!/usr/bin/python
"""
Get the weather information from the open
weather map api
"""
import os
import pprint
import datetime
import json
import urllib2
from utils.parseIni import parseSecretsHere
from utils.lcdI2C import LCD_I2C

class weatherInfo(object):
    config = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config'), 'allConfigurations.ini') 
    secret_config = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config'), 'secrets.ini') 

    def __init__(self):
        self.weatherReport = {}

    def timeConverter(self, time):
        return datetime.datetime.fromtimestamp(
                   int(time)
               ).strftime('%I:%M %p')

    def requestWeather(self):
        self.openWeatherAPI = parseSecretsHere(self.config)
        self.secretKeys= parseSecretsHere(self.secret_config)
        self.openWeatherAPI.parseFileOptions()
        self.secretKeys.parseFileOptions()
        openWeatherMap = self.openWeatherAPI.configuration.get('openWeatherMap', {})
        api = openWeatherMap.get('api', None)
        locations = openWeatherMap.get('locations', None)
        apiKeys = self.secretKeys.configuration.get('APIKeys', {})
        openWeatherMapKey = apiKeys.get('openweathermap', None)
        
        for location in locations.split(','):
            try:
                requestUrl = api + "find?q={0}&type=like&APPID={1}&units=metric".format(location.strip(), openWeatherMapKey)
                weatherResponse = urllib2.urlopen(requestUrl)
            except:
                continue
            self.responseJson = json.loads(weatherResponse.read())
            self.weatherReport[location] = {}
            for values in self.responseJson.get('list', []):
                self.weatherReport[location]['Temp'] = values.get('main', {}).get('temp', None)      
                self.weatherReport[location]['Humidity'] = values.get('main', {}).get('humidity', None)      
                self.weatherReport[location]['Time'] = self.timeConverter(values.get('dt', 0))
                
    def displayOnLCD(self):
        self.requestWeather()
        for location, details in self.weatherReport.items():
            for key, value in details.items():
                msg = key + ":" + str(value)
                LCD_I2C.lcd_byte(0x01, 0)
                LCD_I2C.main(location, msg) 

    def printThemPretty(self):
        pprint.pprint(self.weatherReport)


if __name__ == "__main__":
    s = weatherInfo()
    s.displayOnLCD()
    #s.printThemPretty()
