from bs4 import BeautifulSoup

def extract_headlines(html):

    soup = BeautifulSoup(html, "html.parser")

    headlines = []

    for h in soup.find_all("h2")[:5]:
        headlines.append(h.text.strip())

    return headlines