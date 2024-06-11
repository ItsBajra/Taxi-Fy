from geopy.geocoders import Nominatim

def check_geopy():
    # Create a geolocator object
    geolocator = Nominatim(user_agent="geo_checker")

    # Specify the location you want to check
    location = "New York City, NY"

    try:
        # Try to get the latitude and longitude coordinates of the location
        coordinates = geolocator.geocode(location)
        if coordinates:
            latitude, longitude = coordinates.latitude, coordinates.longitude
            print(f"The coordinates of {location} are: Latitude={latitude}, Longitude={longitude}")
        else:
            print("Location not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_geopy()
