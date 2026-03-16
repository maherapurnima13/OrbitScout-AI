import requests
from bs4 import BeautifulSoup

def get_isro_updates():

    url = "https://www.isro.gov.in"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    headlines = []

    for h in soup.find_all("h2")[:5]:

        headlines.append(h.text.strip())

    return headlines