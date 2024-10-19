# Install Necessary Libraries
!pip install pandas folium kagglehub

# Import Libraries
import pandas as pd
import folium
from folium.plugins import HeatMap
import kagglehub

# Download latest version
path = kagglehub.dataset_download("sudhanvahg/indian-crimes-dataset")
data = pd.read_csv("/kaggle/input/indian-crimes-dataset/crime_dataset_india.csv")

# Display the first few rows of the dataset
print(data.head())

# Check for missing values
print(data.isnull().sum())

# Example of adding latitude and longitude (you'll need actual coordinates)
city_latitude = {'City1': 12.9716, 'City2': 28.7041}  # Add actual city coordinates
city_longitude = {'City1': 77.5946, 'City2': 77.1025}  # Add actual city coordinates

data['Latitude'] = data['City'].apply(lambda x: city_latitude.get(x, None))
data['Longitude'] = data['City'].apply(lambda x: city_longitude.get(x, None))

# Prepare data for HeatMap
heat_data = [[row['Latitude'], row['Longitude'], row['Crime Rate']] for index, row in data.iterrows() if row['Latitude'] and row['Longitude']]

# Create a base map
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)  # Centered on India

# Add HeatMap
HeatMap(heat_data).add_to(m)

# Save the map to an HTML file
m.save('crime_heatmap.html')

# Display the map (if running in a Jupyter notebook or Google Colab)
m

# Analyze crime trends over time
data['Year'] = pd.to_datetime(data['Year'], format='%Y')
yearly_crime_rate = data.groupby('Year')['Crime Rate'].mean().reset_index()

# Create a line plot for crime rate trends
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(yearly_crime_rate['Year'], yearly_crime_rate['Crime Rate'])
plt.title('Crime Rate Trends in India')
plt.xlabel('Year')
plt.ylabel('Average Crime Rate')
plt.grid(True)
plt.savefig('crime_rate_trends.png')
plt.close()

# Identify top 10 cities with highest crime rates
top_10_cities = data.groupby('City')['Crime Rate'].mean().nlargest(10).reset_index()

# Create a bar plot for top 10 cities
plt.figure(figsize=(12, 6))
plt.bar(top_10_cities['City'], top_10_cities['Crime Rate'])
plt.title('Top 10 Cities with Highest Crime Rates')
plt.xlabel('City')
plt.ylabel('Average Crime Rate')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_10_crime_cities.png')
plt.close()

print("Analysis complete. Check 'crime_rate_trends.png' and 'top_10_crime_cities.png' for visualizations.")
