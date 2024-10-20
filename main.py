# Install the required packages if not already installed


import os
import sys
import pandas as pd
import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import time
import json
from google.api_core import retry
import google.generativeai as genai
import seaborn as sns
import numpy as np

# Define the output directory
output_dir = r'E:\Hackathon Projects\MakeATon_Tinkermen\maps'

# Step 1: Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    try:
        os.makedirs(output_dir)
        print(f"Output directory created: {output_dir}")
    except Exception as e:
        print(f"Error creating output directory: {e}")
        sys.exit(1)
else:
    print(f"Output directory already exists: {output_dir}")

# Step 2: Load the dataset
file_path = 'crime_dataset_india.csv'  # Path to the uploaded file
try:
    data = pd.read_csv(file_path)
    print("Data loaded successfully.")
    print(data.head())
except FileNotFoundError:
    print("Error: Unable to find 'crime_dataset_india.csv'. Please check the file path.")
    sys.exit(1)
except Exception as e:
    print(f"Error loading data: {e}")
    sys.exit(1)

# Display column names and check for missing values
print("\nColumns in the dataset:")
print(data.columns)

print("\nMissing values:")
print(data.isnull().sum())

# Step 3: Add latitude and longitude
# Gemini API Key
GOOGLE_API_KEY = "AIzaSyATXE22og8-HoroqLF9J5wlb1l58aHOhhU"

# Configure Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Implement caching
cache_file = 'city_coordinates_cache.json'
try:
    with open(cache_file, 'r') as f:
        city_coordinates = json.load(f)
except FileNotFoundError:
    city_coordinates = {}

@retry.Retry(predicate=retry.if_exception_type(Exception))
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

def get_lat_long_from_gemini(city_name):
    """Function to get latitude and longitude from Gemini API with caching and rate limiting"""
    if city_name in city_coordinates:
        return city_coordinates[city_name]

    try:
        response = get_gemini_response(f"Provide only the latitude and longitude coordinates for {city_name}, India. Format the response as two decimal numbers separated by a comma.")
        lat, lon = map(float, response.split(','))
        city_coordinates[city_name] = (lat, lon)
        
        # Save updated cache
        with open(cache_file, 'w') as f:
            json.dump(city_coordinates, f)
        
        return lat, lon
    except Exception as e:
        print(f"Error fetching coordinates for {city_name}: {e}")
        return None, None

# Populate the city_coordinates dictionary
for city in data['City'].unique():
    if city not in city_coordinates:
        lat, lon = get_lat_long_from_gemini(city)
        if lat and lon:
            city_coordinates[city] = (lat, lon)
        time.sleep(1)  # Add a 1-second delay between API calls

# Add Latitude and Longitude columns
data['Latitude'] = data['City'].map(lambda x: city_coordinates.get(x, (None, None))[0])
data['Longitude'] = data['City'].map(lambda x: city_coordinates.get(x, (None, None))[1])

# Calculate Crime Rate (assuming it's based on the number of crimes per city)
crime_counts = data['City'].value_counts()
data['Crime Rate'] = data['City'].map(crime_counts)

# Prepare data for HeatMap
heat_data = [[row['Latitude'], row['Longitude'], row['Crime Rate']] for index, row in data.iterrows() if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude'])]

# Create a base map centered on India
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

# Add HeatMap layer
HeatMap(heat_data).add_to(m)

# Step 4: Save the map to an HTML file
try:
    map_path = os.path.join(output_dir, 'crime_heatmap.html')
    m.save(map_path)
    print(f"Heatmap saved to: {map_path}")
except Exception as e:
    print(f"Error saving heatmap: {e}")

# Step 5: Identify top 10 cities with highest crime rates
top_10_cities = data.groupby('City')['Crime Rate'].mean().nlargest(10).reset_index()

# Create a bar plot for top 10 cities
plt.figure(figsize=(12, 6))
plt.bar(top_10_cities['City'], top_10_cities['Crime Rate'])
plt.title('Top 10 Cities with Highest Crime Rates')
plt.xlabel('City')
plt.ylabel('Crime Rate')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Step 6: Save the top 10 cities plot
try:
    cities_path = os.path.join(output_dir, 'top_10_crime_cities.png')
    plt.savefig(cities_path)
    plt.close()
    print(f"Top 10 crime cities plot saved to: {cities_path}")
except Exception as e:
    print(f"Error saving top 10 crime cities plot: {e}")

# Step 7: Additional analysis based on the new data structure
# Crime type distribution
crime_type_dist = data['Crime Description'].value_counts().nlargest(10)
plt.figure(figsize=(12, 6))
crime_type_dist.plot(kind='bar')
plt.title('Top 10 Most Common Crime Types')
plt.xlabel('Crime Type')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

try:
    crime_type_path = os.path.join(output_dir, 'top_10_crime_types.png')
    plt.savefig(crime_type_path)
    plt.close()
    print(f"Top 10 crime types plot saved to: {crime_type_path}")
except Exception as e:
    print(f"Error saving top 10 crime types plot: {e}")

# Victim age distribution (improved version)
plt.figure(figsize=(12, 8))
sns.histplot(data['Victim Age'], bins=20, kde=True, color="skyblue", edgecolor="darkblue")

plt.title("Distribution of Victim Ages", fontsize=16, fontweight='bold')
plt.xlabel("Age", fontsize=12)
plt.ylabel("Frequency", fontsize=12)

# Add summary statistics
mean_age = data['Victim Age'].mean()
median_age = data['Victim Age'].median()
plt.axvline(mean_age, color='red', linestyle='dashed', linewidth=2, label=f'Mean Age: {mean_age:.1f}')
plt.axvline(median_age, color='green', linestyle='dashed', linewidth=2, label=f'Median Age: {median_age:.1f}')

plt.legend(fontsize=10)

# Add text for additional statistics
plt.text(0.95, 0.95, f"Total Victims: {len(data)}\nStd Dev: {data['Victim Age'].std():.2f}", 
         transform=plt.gca().transAxes, ha='right', va='top', 
         bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

plt.tight_layout()

try:
    age_dist_path = os.path.join(output_dir, 'victim_age_distribution_improved.png')
    plt.savefig(age_dist_path)
    plt.close()
    print(f"Improved victim age distribution plot saved to: {age_dist_path}")
except Exception as e:
    print(f"Error saving improved victim age distribution plot: {e}")

print(f"Analysis complete. Check {output_dir} for available visualizations.")



import requests
import json

# SheetDB API endpoint
API_URL = "https://sheetdb.io/api/v1/uvztmda65pyb0"

report_number = 40161
def add_row_to_sheet(data):
    """
    Add a single row of data to the spreadsheet.
    
    :param data: A dictionary containing the data to be added
    :return: True if successful, False otherwise
    """
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(API_URL, json=data, headers=headers)
    
    if response.status_code == 201:
        print("Data added successfully!")
        return True
    else:
        print(f"Failed to add data. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def add_multiple_rows(data_list):
    """
    Add multiple rows of data to the spreadsheet.
    
    :param data_list: A list of dictionaries, each containing a row of data
    :return: True if successful, False otherwise
    """
    headers = {
        'Content-Type': 'application/json'
    }
    
    payload = json.dumps({"data": data_list})
    
    response = requests.post(f"{API_URL}/bulk", data=payload, headers=headers)
    
    if response.status_code == 201:
        print(f"Successfully added {len(data_list)} rows of data!")
        return True
    else:
        print(f"Failed to add data. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

# Example usage
if __name__ == "__main__":
    # Adding a single row
    single_row = {
            "Timestamp": "2022-01-02",
            "Report Number": f"{report_number}",
            "City": "Thiruvananthapuram",
            "Crime Code": "102",
            "Crime Description": "VANDALISM",
            "Victim Age": "30",
            "Victim Gender": "F",
            "Weapon Used": "Knife",
            "Crime Domain": "Violent Crime",
            "Police Deployed": "8",
            "Case Closed": "Yes"
    }
    add_row_to_sheet(single_row)
    report_number += 1
    

    