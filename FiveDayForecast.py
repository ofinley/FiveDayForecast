# Author: Joseph Finley
# Open Weather Map API
#
# Purpose: Take user supplied zip code and make
#          an API call for a 5 day forcast.
#
#

import requests, calendar
from collections import Counter

# Forecast Object to organize data from request
class Forecast():
    
    def __init__(self,date):
        self.date = date
        self.temps = []
        self.high_temps = []
        self.low_temps = []
        self.precip = []
        self.description = ''
        self.description_list = []
        self.winds = []

    def addTemps(self, temp):
        self.temps.append(temp)

    def addHighTemps(self, htemp):
        self.high_temps.append(htemp)

    def addLowTemps(self, ltemp):
        self.low_temps.append(ltemp)

    def addPrecip(self, rain):
        self.precip.append(rain)

    def addWind(self,wind):
        self.winds.append(wind)

    def addDescrip(self, desc):
        self.description_list.append(desc)

    # Get the most occuring description of the day
    def setDescription(self):
        c = Counter(self.description_list)
        cmc = c.most_common(1)
        self.description = cmc[0][0]
        

    # Display Date, High temps, Low temps, total precipitation and most occuring
    # description for each day   
    def __repr__(self):
        self.setDescription()
        return '{}           {}/{}                   {:01.02f}                  {:01.02f}             {} '.format(
                self.date,
                max(self.high_temps),
                min(self.low_temps),
                sum(map(float,self.precip)),
                (sum(self.winds)/len(self.winds)),
                self.description)

        
# Print out the 5 day forecast with headers
def neatPrint(final):
    # Get length of final list
    length = len(final)

    # Print Header first
    print('\n# Date           Temperature(Fahrenheit)   Precipitation(mm)  Avg. Wind Speed(m/s)     Description\n')

    # Print out each item in final list
    for item in range(length):
        print('#', forecast_list[item])

    # For the extra space at the bottom
    print('\n') 
     

# API Key here
api_key = 'f03da4c051db7f056f4207292166bf9f'

# API call that will have user input zipcode append to
api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key

# Check input to make sure it is a number and the correct length of a zipcode
while True:
    try:

        # Request Zipcode from user
        print('Please Enter Zipcode (USA only):')
        zipcode = int(input())

    except ValueError:
        print('Error: Input must be a number. Please try again!')
        continue
        
    if len(str(zipcode)) > 5 or len(str(zipcode)) < 5:
        print('Zipcode must be exactly five digits.')
        continue

    else:
        break


# Append zipcode to API Call
api_call += '&zip=' + str(zipcode)

# Request and store data
data = requests.get(api_call).json()

# Current date string for iteration
current_date = ''

# Create list of Forecast objects to collect dates with their temperatures and precipitation
forecast_list = []

# Get the city and country
city = data['city']['name']
country = data['city']['country']
print('\nCity & Country: ' + city + ', ' + country + '\n')


# Iterate through the data from JSON request
# and work with the data
for i in data['list']:

    # Get date and change format to mm/dd/yyyy
    raw_date = i['dt_txt']
    next_date, time = raw_date.split(' ')
    if  current_date != next_date: 
        current_date = next_date
        year, month, day = current_date.split('-')
        date = {'m': month, 'd':day, 'y':year}
    
        # Create new Forecast object with new date
        # and append to forecast list
        forecast = Forecast('{m}/{d}/{y}'.format(**date))
        forecast_list.append(forecast)


    # Add all temperatures associated with the same date. All temps are in Kelvin by default
    temp = i['main']['temp']
    forecast.addTemps('{:01.0f}'.format(temp*(9/5)-459.67))

    # Add all high temperatures within the same date
    htemp = i['main']['temp_max']
    forecast.addHighTemps('{:01.0f}'.format(htemp*(9/5)-459.67))

    # Add all low temperatures within the same date
    ltemp = i['main']['temp_min']
    forecast.addLowTemps('{:01.0f}'.format(ltemp*(9/5)-459.67))

    # Add Descriptions of weather
    descriptions = i['weather'][0]['description']
    forecast.addDescrip(descriptions)

    # Add Wind speeds default is in Metric
    windSpeed = i['wind']['speed']
    forecast.addWind(windSpeed)


    # Check if there is any Precipitation, else report 0
    if 'rain' in i:
        precipitation = i['rain']['3h']
        forecast.addPrecip('{:01.002f}'.format(precipitation))      
    else:
        forecast.addPrecip('{:01.002f}'.format(0))
 

# Print final results 
neatPrint(forecast_list)
print('Finished!')




