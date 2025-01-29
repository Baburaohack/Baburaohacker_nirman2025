import requests
import random
import time

# Predefined list of major Indian cities with their latitude and longitude
locations = {
    'Mumbai': (19.0760, 72.8777),
    'Delhi': (28.6139, 77.2090),
    'Bengaluru': (12.9716, 77.5946),
    'Hyderabad': (17.3850, 78.4867),
    'Chennai': (13.0827, 80.2707),
    'Kolkata': (22.5726, 88.3639),
    'Ahmedabad': (23.0225, 72.5714),
    'Pune': (18.5204, 73.8567),
    'Jaipur': (26.9124, 75.7873),
    'Surat': (21.1702, 72.8311),
    'Lucknow': (26.8467, 80.9462),
    'Kanpur': (26.4499, 80.3319),
    'Nagpur': (21.1458, 79.0882),
    'Visakhapatnam': (17.6868, 83.2185),
    'Bhopal': (23.2599, 77.4126),
    'Indore': (22.7196, 75.8577),
    'Coimbatore': (11.0168, 76.9558),
    'Patna': (25.5941, 85.1376),
    'Vadodara': (22.3072, 73.1812),
    'Ludhiana': (30.9009, 75.8573),
    'Agra': (27.1767, 78.0081),
    'Nashik': (19.9975, 73.7898),
    'Faridabad': (28.4082, 77.3178),
    'Meerut': (28.9845, 77.7066),
    'Rajkot': (22.3039, 70.8022),
    'Kalyan-Dombivli': (19.2183, 73.1528),
    'Vijayawada': (16.5062, 80.6480),
    'Mysuru': (12.2958, 76.6393),
    'Jodhpur': (26.2389, 73.0243),
    'Dehradun': (30.3165, 78.0322),
    'Ranchi': (23.3569, 85.3340),
    'Guwahati': (26.1445, 91.7362),
    'Agartala': (23.8315, 91.2868),
    'Srinagar': (34.0836, 74.7973),
    'Imphal': (24.8170, 93.9368),
    'Shillong': (25.5788, 91.8932),
    'Aizawl': (23.1645, 92.9376),
    'Kohima': (25.6700, 94.1120),
    'Itanagar': (27.1025, 93.6150),
}

# Function to fetch external temperature from Open-Meteo
def fetch_external_temperature(latitude, longitude):
    try:
        # Fetch weather data using Open-Meteo API
        response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true')
        weather_data = response.json()
        
        if 'current_weather' in weather_data:
            current_temp = weather_data['current_weather']['temperature']  # Temperature in Celsius
            return current_temp
        else:
            print(f"Error fetching weather data: {weather_data}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to generate internal temperature
def generate_internal_temperature():
    # Simulate internal temperature between 60 and 100 degrees Celsius
    return random.uniform(60, 100)

# Main loop
def main():
    print("Select your current location:")
    for index, city in enumerate(locations.keys(), start=1):
        print(f"{index}. {city}")

    # Get user selection
    choice = int(input("Enter the number corresponding to your location: ")) - 1
    selected_city = list(locations.keys())[choice]
    latitude, longitude = locations[selected_city]

    print(f"You selected: {selected_city} (Lat: {latitude}, Lon: {longitude})")

    while True:
        internal_temp = generate_internal_temperature()
        external_temp = fetch_external_temperature(latitude, longitude)

        if external_temp is not None:
            print(f"Internal Temperature: {internal_temp:.2f} °C")
            print(f"External Temperature: {external_temp:.2f} °C")

            # Compare temperatures
            if internal_temp > external_temp + 5:  # Example threshold
                print("Warning: Internal temperature is significantly higher than external temperature.")
            else:
                print("Internal temperature is within acceptable range.")

            print("-" * 40)

        time.sleep(10)  # Wait for 10 seconds before the next reading

if __name__ == "__main__":
    main()
  
