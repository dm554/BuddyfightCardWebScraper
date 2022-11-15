import requests
from bs4 import BeautifulSoup


# Gets card ability information from wiki page
def get_card_ability(tag):
    card_text = tag.findAll(name="tr")
    card_list = []

    for line in card_text:
        card_lines = line.get_text(separator=" ", strip=True)
        card_list.append(card_lines)

    ability_index = card_list.index('Ability / Effect') + 1
    return card_list[ability_index]


# Gets specific card information from wiki page
def get_card_info(tag):
    card_stats = tag.findAll(name="table", class_="main")
    stats_list = []

    for stat in card_stats:
        stats = stat.get_text(separator=",", strip=True)
        stats_list = stats.split(",")

    stats_list.append(get_card_ability(tag))
    return stats_list


# Get Request for Webpage
response = requests.get("https://buddyfight.fandom.com/wiki/Drum_Bunker_Dragon")

if response.status_code != 200:
    print("Error fetching page")
    exit()
else:
    content = response.content

soup = BeautifulSoup(response.content, 'html.parser')

print(get_card_info(soup))






