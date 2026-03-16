from crawlers.nasa_crawler import get_nasa_news
from crawlers.isro_crawler import get_isro_updates
from crawlers.spacex_crawler import get_spacex_launches


def collect_intelligence():

    nasa = get_nasa_news()
    isro = get_isro_updates()
    spacex = get_spacex_launches()

    return {
        "nasa_updates": nasa,
        "isro_updates": isro,
        "spacex_launches": spacex
    }