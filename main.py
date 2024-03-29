import requests
import card
import json
import sys
from bs4 import BeautifulSoup


# Get Request for Webpage
def card_page_init(card_webpage):
    response = requests.get(card_webpage)
    if response.status_code != 200:
        print("Error fetching page")
        exit()
    else:
        content = response.content
    return BeautifulSoup(response.content, 'html.parser')


# Returns list card URLs to be searched from set table
def card_urls(tag):
    url_list = []

    table = tag.find('table', class_='wikitable')
    for row in table.find_all('a'):
        href = row['href']
        url_list.append(href)
    return url_list


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
        stats = stat.get_text(separator=";", strip=True)
        stats_list = stats.split(";")

    stats_list.append(get_card_ability(tag))
    return stats_list


# Getting Card types from wiki page (Monster, Spell, Impact)
def get_card_type(tag):
    card_type = None
    if tag.find(name='a', string="Monster") is not None:
        card_type = "Monster"
    elif tag.find(name='a', string="Spell") is not None:
        card_type = "Spell"
    elif tag.find(name='a', string="Impact") is not None:
        card_type = "Impact"
    elif tag.find(name='a', string="Item") is not None:
        card_type = "Item"

    return card_type

#Gets a list of card attributes
def grab_card_attributes(info):
    startIndex = info.index("Attribute") + 1
    if "Illust" in info or "Design / Illust" in info:
        if "Illust" in info:
            endIndex = info.index("Illust")
        elif "Design / Illust" in info:
            endIndex = info.index("Design / Illust")
    else:
        endIndex = -1
    attribute_list = info[startIndex : endIndex]
    attributes = attribute_list[::2]
    return attributes



# Creates a card object based on card type and adds to list
# Make this function modular
def card_create(tag, c_list):
    card_type = get_card_type(tag)
    info = get_card_info(tag)
    attribute = grab_card_attributes(info)
    
    if card_type == "Monster":
        if info[2] == "Kanji" and info[4] == "Kana":
            c_list.append(card.Monster(info[1], info[19], info[11], info[13], info[15], info[17], info[-1], attribute).__dict__)
        else:
            c_list.append(card.Monster(info[1], info[17], info[9], info[11], info[13], info[15], info[-1], attribute).__dict__)
    elif card_type == "Spell":
        if info[2] == "Kanji" and info[4] == "Kana":
            if(info[8] == "Translated"):
                c_list.append(card.Spell(info[1], info[13], info[-1], attribute).__dict__)
            else:
                c_list.append(card.Spell(info[1], info[11], info[-1], attribute).__dict__)
            
        else:
            c_list.append(card.Spell(info[1], info[9], info[-1], attribute).__dict__)
    elif card_type == "Impact":
        c_list.append(card.Impact(info[1], info[11], info[-1], attribute).__dict__)
    elif card_type == "Item":
        c_list.append(card.Item(info[1], info[15], info[11], info[13], info[-1], attribute).__dict__)



soup = card_page_init(str(sys.argv[1]))
card_url_list = card_urls(soup)
card_url_list = card_url_list[1::3]
card_list = []

#Iterates through Card URLs in Set and Creates Card Objects
for url in card_url_list:
    soup = card_page_init("https://buddyfight.fandom.com/" + url)
    card_create(soup, card_list)


#Opens/Creates json File and Dumps Card Objects
jsonFileName = str(sys.argv[1]).split('/')[-1].replace(":", "") + ".json"
with open("card_set_data/"+ jsonFileName, 'w') as f:
    json.dump(card_list, f, indent=4)

print("\n--Set Completed--\n")
