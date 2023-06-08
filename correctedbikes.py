import streamlit as st
import time
# stdlib imports
import json
import pandas as pd

# third-party imports (may need installing)
import requests
import csv
import math

with st.form("my_form"):
   st.write("Find the Nearest Bike to your Location")
 
   given_lat = st.number_input('Insert your Latitude', format='%f', step=0.000001)
   given_long = st.number_input('Insert your longitude', format='%f', step=0.000001)

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")

# Creating csv file
myfile = open('BikeStations.csv', 'w', newline='')
csvwriter = csv.writer(myfile) # create a csvwriter object
csvwriter.writerow(['ID', 'totalSlotNumber', 'City', 'Street', 'Longitude', 'Latitude']) # write the header

data = []  # Initialize list to hold extracted coordinates

for i in range(1, 60): 
    # Formating URL
    addedstr = str(i)
    if i < 9:
        addedstr = '0' + addedstr
    url = 'https://portail-api-data.montpellier3m.fr/bikestation?id=urn%3Angsi-ld%3Astation%3A0' + addedstr + '&limit=1'
    # Sending request
    response = requests.get(url)

    # Translating byte response to Python data structures
    response_json = response.json()
    if len(response_json) > 0:
        ## Print Raw Data
        #print(response_json)

        # Extracting data from Json
        data.append([
            response_json[0]['id'].replace(":", "%3"),
            response_json[0]['totalSlotNumber']['value'],
            response_json[0]['address']['value']['addressLocality'],
            response_json[0]['address']['value']['streetAddress'],
            response_json[0]['location']['value']['coordinates'][0],
            response_json[0]['location']['value']['coordinates'][1]
        ])
   
        # Print Extracted data
        #print(data)

        # Wrinting Values in csv
        csvwriter.writerow(data[-1]) # write the latest row

myfile.close()

def calculate_distance(lati, long, compcoord):
    x2, y2 = compcoord
    print(x2,y2)
    return math.sqrt((x2 - lati) ** 2 + (y2 - long) ** 2)


#distance =R∗cos−1(cos(ϕ1)cos(ϕ2)cos(λ1−λ2)+sin(ϕ1)sin(ϕ2))


min_distance = float('inf')
closest_coord = None

for coord in data:
    distance = calculate_distance(given_long, given_lat, coord[4:])
    if distance < min_distance:
        min_distance = distance
        closest_coord = coord

if submitted:
    st.write('You typed the coordinates: ', given_lat, given_long)
    st.write('The nearest bike to your location is at: ',closest_coord[3], ", " , closest_coord[2], ", " ,closest_coord[4], ", ", closest_coord[5])
    st.write('It is ', min_distance, ' km away')
    #st.write('There are ' ' bikes available here.')



st.write("Map")
st.write(time.asctime(time.localtime()))
print( [closest_coord[4], closest_coord[5]])
print( given_lat, given_long)

# Create a DataFrame with the inputted coordinates and the closest coordinate
map_data = pd.DataFrame([[given_long,given_lat], [closest_coord[4], closest_coord[5]]], columns=['lon', 'lat'])

st.map(map_data)

#dabikes = pd.read_csv('BikeStations.csv', usecols=['Longitude', 'Latitude'])
#dabikes.columns = ['lon', 'lat']
    
#st.map(dabikes)





#-----------------------
#account on github 
