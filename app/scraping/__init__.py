import requests
from bs4 import BeautifulSoup
import re


class ScrapingMagicEmperor:
    name = "Mo Huang Da Guan Jia – Magic Emperor"
    last_chapter = ""
    link = ""
    url_request = "https://imperiodabritannia.com/manga/magic-emperor/ajax/chapters/"

    def __init__(self) -> None:
        try:
            with requests.post(self.url_request) as response:
                if response.status_code == 200:
                    self.response = response.content
                else:
                    self.response = ""
        except requests.ConnectTimeout:
            self.__init__()

    def get_data(self) -> dict:
        html_page = self.response

        soup = BeautifulSoup(html_page, "html.parser")
        chapters = soup.find_all("li", class_="wp-manga-chapter")

        last_capther_elem = chapters[0]
        link = last_capther_elem.find("a").attrs["href"]

        last_capther = last_capther_elem.text
        last_capther = re.findall(r"Cap. (\d+)", last_capther)[0]

        self.last_chapter = last_capther
        self.link = link

        data = {"name": self.name, "last_chapter": self.last_chapter, "link": self.link}
        return data
