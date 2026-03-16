import requests
from bs4 import BeautifulSoup

def get_nasa_news():

    url = "https://www.nasa.gov/news/"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    for item in soup.find_all("h2")[:5]:

        results.append(item.text.strip())

    return results