import requests
from bs4 import BeautifulSoup

url_search_results = 'https://www.kiwi.com/co/search/results/bogota-colombia/cali-colombia/2024-01-27/2024-02-02'

response = requests.get(url_search_results)


if response.status_code == 200:
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract flight details
    flight_elements = soup.find_all('div', class_='your-flight-class')  
    print("Page Title:", soup.title.text)
    
    for flight_element in flight_elements:
        # Extract relevant information from each flight element
        departure_time = flight_element.find('span', class_='departure-time').text
        arrival_time = flight_element.find('span', class_='arrival-time').text
        airline = flight_element.find('span', class_='airline').text
        price = flight_element.find('span', class_='price').text


        # Print or store the extracted information
        print(f"Departure Time: {departure_time}, Arrival Time: {arrival_time}, Airline: {airline}, Price:{price}")

else:
    print("Error while making the request. Status code:", response.status_code)
