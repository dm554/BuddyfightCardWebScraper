import requests
from bs4 import BeautifulSoup


# Scrapes all the card data
def get_card_info(tag):
    return tag.name == "table" and tag.has_attr("class") and "main" in tag.get("class")


# Get Request
response = requests.get("https://buddyfight.fandom.com/wiki/Drum_Bunker_Dragon")
if response.status_code != 200:
    print("Error fetching page")
    exit()
else:
    content = response.content


soup = BeautifulSoup(response.content, 'html.parser')

print(soup.findAll(get_card_info))
