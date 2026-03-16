import requests
from bs4 import BeautifulSoup

def get_spacex_launches():

    url = "https://www.spacex.com/launches/"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    launches = []

    for item in soup.find_all("h3")[:5]:

        launches.append(item.text.strip())

    return launches