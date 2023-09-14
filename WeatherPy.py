#!/usr/bin/env python
# coding: utf-8

# # WeatherPy
# 
# ---
# 
# ## Starter Code to Generate Random Geographic Coordinates and a List of Cities

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
from scipy.stats import linregress

# Impor the OpenWeatherMap API key
from api_keys import weather_api_key

# Import citipy to determine the cities based on latitude and longitude
from citipy import citipy


# ### Generate the Cities List by Using the `citipy` Library

# In[2]:


# Empty list for holding the latitude and longitude combinations
lat_lngs = []

# Empty list for holding the cities names
cities = []

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)

# Create a set of random lat and lng combinations
lats = np.random.uniform(lat_range[0], lat_range[1], size=1500)
lngs = np.random.uniform(lng_range[0], lng_range[1], size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
print(f"Number of cities in the list: {len(cities)}")


# ---

# ## Requirement 1: Create Plots to Showcase the Relationship Between Weather Variables and Latitude
# 
# ### Use the OpenWeatherMap API to retrieve weather data from the cities list generated in the started code

# In[3]:


# Set the API base URL
url = "http://api.openweathermap.org/data/2.5/weather?"
units = "metric"

# Define an empty list to fetch the weather data for each city
city_data = []

# Print to logger
print("Beginning Data Retrieval     ")
print("-----------------------------")

# Create counters
record_count = 1
set_count = 1

# Loop through all the cities in our list to fetch weather data
for i, city in enumerate(cities):
        
    # Group cities in sets of 50 for logging purposes
    if (i % 50 == 0 and i >= 50):
        set_count += 1
        record_count = 0

    # Create endpoint URL with each city
    city_url = f"{url}appid={weather_api_key}&units={units}&q="
    
    # Log the url, record, and set numbers
    print("Processing Record %s of Set %s | %s" % (record_count, set_count, city))

    # Add 1 to the record count
    record_count += 1

    # Run an API request for each of the cities
    try:
        # Parse the JSON and retrieve data
        city_weather = requests.get(city_url + city).json()

        # Parse out latitude, longitude, max temp, humidity, cloudiness, wind speed, country, and date
        city_lat = city_weather["coord"]["lat"]
        city_lng = city_weather["coord"]["lon"]
        city_max_temp = city_weather["main"]["temp_max"]
        city_humidity = city_weather["main"]["humidity"]
        city_clouds = city_weather["clouds"]["all"]
        city_wind = city_weather["wind"]["speed"]
        city_country = city_weather["sys"]["country"]
        city_date = city_weather["dt"]

        # Append the City information into city_data list
        city_data.append({"City": city, 
                          "Lat": city_lat, 
                          "Lng": city_lng, 
                          "Max Temp": city_max_temp,
                          "Humidity": city_humidity,
                          "Cloudiness": city_clouds,
                          "Wind Speed": city_wind,
                          "Country": city_country,
                          "Date": city_date})

    # If an error is experienced, skip the city
    except:
        print("City not found. Skipping...")
        pass
              
# Indicate that Data Loading is complete 
print("-----------------------------")
print("Data Retrieval Complete      ")
print("-----------------------------")


# In[4]:


# Convert the cities weather data into a Pandas DataFrame
city_data_df = pd.DataFrame(city_data)

# Show Record Count
city_data_df.count()


# In[5]:


# Display sample data
city_data_df.head()


# In[6]:


# Export the City_Data into a csv
city_data_df.to_csv("output_data/cities.csv", index_label="City_ID")


# In[7]:


# Read saved data
city_data_df = pd.read_csv("output_data/cities.csv", index_col="City_ID")

# Display sample data
city_data_df.head()


# ### Create the Scatter Plots Requested
# 
# #### Latitude Vs. Temperature

# In[8]:


# Build scatter plot for latitude vs. temperature
plt.scatter(city_data_df["Lat"], 
            city_data_df["Max Temp"], 
            marker="o",
            edgecolor="black",
            linewidths=1,
            label="cities",
            alpha=0.8
)

# Incorporate the other graph properties
import time
date = time.strftime("%Y-%m-%d")
plt.title(f"City Max Latitude vs. Temperature ({date})")
plt.xlabel("Latitude")
plt.ylabel("Max Temperature (C)")
plt.grid(True)

# Save the figure
plt.savefig("output_data/Fig1.png")

# Show plot
plt.show()


# #### Latitude Vs. Humidity

# In[9]:


# Build the scatter plots for latitude vs. humidity
plt.scatter(city_data_df["Lat"], 
            city_data_df["Humidity"], 
            marker="o",
            edgecolor="black",
            linewidths=1,
            label="cities",
            alpha=0.8
)

# Incorporate the other graph properties
date = time.strftime("%Y-%m-%d")
plt.title(f"City Latitude vs. Humidity ({date})")
plt.xlabel("Latitude")
plt.ylabel("Humidity (%)")
plt.grid(True)

# Save the figure
plt.savefig("output_data/Fig2.png")

# Show plot
plt.show()


# #### Latitude Vs. Cloudiness

# In[10]:


# Build the scatter plots for latitude vs. cloudiness
plt.scatter(city_data_df["Lat"], 
            city_data_df["Cloudiness"], 
            marker="o",
            edgecolor="black",
            linewidths=1,
            label="cities",
            alpha=0.8
)

# Incorporate the other graph properties
plt.title(f"City Latitude vs. Cloudiness ({date})")
plt.xlabel("Latitude")
plt.ylabel("Cloudiness (%)")
plt.grid(True)

# Save the figure
plt.savefig("output_data/Fig3.png")

# Show plot
plt.show()


# #### Latitude vs. Wind Speed Plot

# In[11]:


# Build the scatter plots for latitude vs. wind speed
plt.scatter(city_data_df["Lat"], 
            city_data_df["Wind Speed"], 
            marker="o",
            edgecolor="black",
            linewidths=1,
            label="cities",
            alpha=0.8
)

# Incorporate the other graph properties
plt.title(f"City Latitude vs. Wind Speed ({date})")
plt.xlabel("Latitude")
plt.ylabel("Wind Speed (m/s)")
plt.grid(True)

# Save the figure
plt.savefig("output_data/Fig4.png")

# Show plot
plt.show()


# ---
# 
# ## Requirement 2: Compute Linear Regression for Each Relationship
# 

# In[12]:


# Define a function to create Linear Regression plots

def plot_linear_regression(x_values, y_values, title, text_coord):

    (slope, intercept, rvalue, pvalue, stderr) = linregress(x_values,y_values)
    regress_values = x_values * slope + intercept
    line_eq = f"y = {round(slope, 2)}x + {round(intercept, 2)}"
    
    plt.scatter(x_values, y_values)
    plt.plot(x_values, regress_values, "r-")
    
    plt.xlabel("Latitude")
    plt.ylabel(title)

    plt.annotate(line_eq, text_coord, fontsize=15, color="red")
    print(f"The r-value is: {rvalue**2}")
    
    plt.show()


# In[13]:


# Create a DataFrame with the Northern Hemisphere data (Latitude >= 0)
northern_hemi_df = city_data_df.loc[city_data_df["Lat"] >= 0]

# Display sample data
northern_hemi_df.head()


# In[14]:


# Create a DataFrame with the Southern Hemisphere data (Latitude < 0)
southern_hemi_df = city_data_df.loc[city_data_df["Lat"] < 0]

# Display sample data
southern_hemi_df.head()


# ###  Temperature vs. Latitude Linear Regression Plot

# In[15]:


# Linear regression on Northern Hemisphere
x_values = northern_hemi_df["Lat"]
y_values = northern_hemi_df["Max Temp"]

plot_linear_regression(x_values, y_values, "Max Temp", (5,5))


# In[16]:


# Linear regression on Southern Hemisphere
x_values = southern_hemi_df["Lat"]
y_values = southern_hemi_df["Max Temp"]

plot_linear_regression(x_values, y_values, "Max Temp", (-55,30))


# **Discussion about the linear relationship:** The r-value calculated for the northern and southern hemisphere max temperature vs. latitude are greater than 0.5, which is a strong correlation between the two variables. The closer the latitude corrdinates are to 0 degrees, which is the equator, the greater the temperature is in that city compared to those further from the equator.

# ### Humidity vs. Latitude Linear Regression Plot

# In[23]:


# Northern Hemisphere
x_values = northern_hemi_df["Lat"]
y_values = northern_hemi_df["Humidity"]

plot_linear_regression(x_values, y_values, "Humidity", (45,15))


# In[18]:


# Southern Hemisphere
x_values = southern_hemi_df["Lat"]
y_values = southern_hemi_df["Humidity"]

plot_linear_regression(x_values, y_values, "Humidity", (-55,15))


# **Discussion about the linear relationship:** The r-value calculated for the northern and southern hemisphere humidity vs. latitude were less than 0.1, which is a weak correlation between the two variables. Therefore, humidity is about the same across the cities within the northern hemisphere regardless of the latitude value. The same goes for the cities in the southern hemisphere.
# 
# The humidity for majority of the cities within the northern hemispheres is around 80 -100%. The humidity for the cities in the southern hemisphere is about evenly distributed with majority of the cities with humidity of about 60 - 90%.

# ### Cloudiness vs. Latitude Linear Regression Plot

# In[19]:


# Northern Hemisphere
x_values = northern_hemi_df["Lat"]
y_values = northern_hemi_df["Cloudiness"]

plot_linear_regression(x_values, y_values, "Cloudiness", (45,10))


# In[20]:


# Southern Hemisphere
x_values = southern_hemi_df["Lat"]
y_values = southern_hemi_df["Cloudiness"]

plot_linear_regression(x_values, y_values, "Cloudiness", (-55,5))


# **Discussion about the linear relationship:** The r-value calculated for the northern and southern hemisphere cloudiness vs. latitude were less than 0.1, which is a weak correlation between the two variables. Therefore, cloudiness is about the same across the cities within the northern hemisphere regardless of the latitude value. The same goes for the cities in the southern hemisphere.
# 
# The cloudiness in the cities within both hemispheres are about evenly distributed on a scale of 0 - 100%.

# ### Wind Speed vs. Latitude Linear Regression Plot

# In[21]:


# Northern Hemisphere
x_values = northern_hemi_df["Lat"]
y_values = northern_hemi_df["Wind Speed"]

plot_linear_regression(x_values, y_values, "Wind Speed", (45,12))


# In[22]:


x_values = southern_hemi_df["Lat"]
y_values = southern_hemi_df["Wind Speed"]

plot_linear_regression(x_values, y_values, "Wind Speed", (-50,13))


# **Discussion about the linear relationship:** The r-value calculated for the northern and southern hemisphere wind speed vs. latitude were less than 0.1, which is a weak correlation between the two variables. Therefore, wind speed is about the same across the cities within the northern hemisphere regardless of the latitude value. The same goes for the cities in the southern hemisphere.
# 
# The wind speed in majority of the cities within both hemispheres is about 0 - 7 m/s.

# In[ ]:




