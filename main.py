import requests
import card
from bs4 import BeautifulSoup


# Gets card ability/effect information from wiki page
def get_card_ability(tag):
    card_text = tag.findAll(name="tr")
    card_text_list = []

    for line in card_text:
        card_lines = line.get_text(separator=" ", strip=True)
        card_text_list.append(card_lines)

    ability_index = card_text_list.index('Ability / Effect') + 1
    return card_text_list[ability_index]


# Gets specific card information from wiki page
def get_card_info(tag):
    card_stats = tag.findAll(name="table", class_="main")
    stats_list = []

    for stat in card_stats:
        stats = stat.get_text(separator=",", strip=True)
        stats_list = stats.split(",")

    stats_list.append(get_card_ability(tag))
    return stats_list


# Getting Card types from wiki page (Monster, Spell, Impact)
def get_card_type(tag):
    card_type = tag.find(name='a', string="Monster").get_text()
    return card_type


# Creates a card object based on card type and adds to list
def card_create(tag, c_list):
    card_type = get_card_type(tag)
    info = get_card_info(tag)
    if card_type == "Monster":
        c_list.append(card.Monster(info[1], info[17], info[9], info[11], info[13], info[15], info[-1]))


card_webpage = "https://buddyfight.fandom.com/wiki/Drum_Bunker_Dragon"

# Get Request for Webpage
response = requests.get(card_webpage)
if response.status_code != 200:
    print("Error fetching page")
    exit()
else:
    content = response.content

soup = BeautifulSoup(response.content, 'html.parser')
card_list = []

card_create(soup, card_list)

# iterates through list of card objects and prints data
for card in card_list:
    print(card.__str__())







