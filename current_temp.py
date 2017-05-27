####################################################
#                   Current Temp
# This program using web scraping to get the city,
# state, and current temperature from a zip code.
# The program prompts the user for a zip code then
# scrapes the latitude/longtitude and also city/state
# from melissadata.com. Then the current temperature
# is retrieved from weather.gov using the collected
# data.  
####################################################
import requests
import bs4


####################################################
#               Check Input Function
# Checks the input provided by the user. The input
# should contain 5 characters and they should all
# be of data type integers. Returns True if all
# the input tests are passed.
#
# Parameters: zip_code - user provided zip code
####################################################
def check_input(zip_code):
    test = '0123456789'
    for letter in zip_code:
        if letter not in test:
            print("Input must only contain integers...")
            return False
    if not len(zip_code) == 5:
        print("Input must contain 5 digits...")
        return False
    return True


####################################################
#                Get the Lat and Long
# Takes a zip code and checks melissadata.com for
# the latitude and longtitude that matches. Returns
# a list made up of the latitude in the 0 index and
# a longtitude in the 1 index.
#
# Parameters: zip_code - user provided zip code
####################################################
def get_lat_long(zip_code):
    zip_site = ('https://www.melissadata.com/lookups/GeoCoder.asp?InData=' +
                zip_code + '&submit=Search')
    zip_check = requests.get(zip_site)

    try:
        zip_check.raise_for_status()
    except Exception as exc:
        print("There was a problem: %s" % (exc))

    check_zip = bs4.BeautifulSoup(zip_check.text, 'html.parser')
    lat_long = check_zip.select('td')
    info = [lat_long[13].getText(), lat_long[15].getText()]
    return info


####################################################
#             Finds the City and State
# Takes the zip code entered by the user and returns
# the city and the state in a list. The city is index
# 0 and the state is index 1.
#
# Parameters: zip_code - user provided zip code
####################################################
def city_state(zip_code):
    url = ('https://www.melissadata.com/lookups/' +
           'ZipCityPhone.asp?InData=' + zip_code)
    request = requests.get(url)

    try:
        request.raise_for_status()
    except Exception as exc:
        print("There was a problem: %s" % (exc))

    html = bs4.BeautifulSoup(request.text, 'html.parser')
    scrape = html.select('td')

    temp_state = scrape[13].getText()
    city = scrape[17].getText()

    if contains_multiple_words(city):
        city, extra = city.split()

    first_letter = city[0]
    city = city.replace(first_letter, "")
    city = city.lower()
    city = first_letter + city
    full_state_name, abbrev_state = temp_state.split(" ")
    city_state = [city, full_state_name]
    return city_state


####################################################
#                Checks for 2 Words
# Takes a string and returns true if the string
# contains more than one word.
#
# Parameters: word - string to be checked
####################################################
def contains_multiple_words(word):
    return len(word.split()) > 1


# Program Header
print("---Check the temperature of your area---")
zip_code = raw_input("Please enter a zip code:")
while not check_input(zip_code):
    zip_code = raw_input("Error..Please enter a valid zip code: ")

lat_long = get_lat_long(zip_code)

# requests a download from weather.gov
site = ('http://forecast.weather.gov/MapClick.php?lat='
        + lat_long[0] + '&lon=' + lat_long[1])
weather = requests.get(site)

# tries for error when opening the website
try:
    weather.raise_for_status()
except Exception as exc:
    print("There was a problem: %s" % (exc))

# loads the correct tag from weather.com into weather_str
check_weather = bs4.BeautifulSoup(weather.text, 'html.parser')
temp = check_weather.select('.myforecast-current-lrg')

city_and_state = city_state(zip_code)

# prints out the temperature of the zip code
print ('The current temperature for ' + city_and_state[0] + ", " +
       city_and_state[1] + ' is ' + temp[0].getText() + '.')
