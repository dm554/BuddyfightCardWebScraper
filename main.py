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
    if table is None:
        table = tag.find('table', class_='MsoTableGrid')

    for row in table.find_all('a'):
        href = row['href']
        url_list.append(href)
        #print(url_list)
    return url_list


# Gets card ability/effect information from wiki page
def get_card_ability(tag):
    card_text = tag.findAll(name="tr")
    card_text_list = []

    for line in card_text:
        card_lines = line.get_text(separator=" ", strip=True)
        card_text_list.append(card_lines)

    if 'Ability / Effect' in card_text_list:
        ability_index = card_text_list.index('Ability / Effect') + 1
        return card_text_list[ability_index]
    else:
        abl_text = ''
        return card_text_list[-1:]


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
    elif tag.find(name='a', string="Flag") is not None:
        card_type = "Flag"

    return card_type

#Gets a list of card attributes
def grab_card_attributes(info):
    print(info)
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
    if card_type != "Flag":
        attribute = grab_card_attributes(info)

    if card_type == "Flag":
        c_list.append(card.Flag(info[info.index("English") + 1],
                                info[info.index("World") + 1],
                                info[-1]).__dict__)
    elif card_type == "Monster":
        c_list.append(card.Monster(info[info.index("English") + 1],
                                   info[info.index("World") + 1],
                                   info[info.index("Size") + 1],
                                   info[info.index("Power") + 1],
                                   info[info.index("Critical") + 1],
                                   info[info.index("Defense") + 1],
                                   info[-1],
                                   attribute).__dict__)
    elif card_type == "Spell":
        c_list.append(card.Spell(info[info.index("English") + 1],
                                 info[info.index("World") + 1],
                                 info[-1],
                                 attribute).__dict__)
    elif card_type == "Impact":
        c_list.append(card.Impact(info[info.index("English") + 1],
                                  info[info.index("World") + 1],
                                  info[-1],
                                  attribute).__dict__)
    elif card_type == "Item":
        c_list.append(card.Item(info[info.index("English") + 1],
                                info[info.index("World") + 1],
                                info[info.index("Power") + 1],
                                info[info.index("Critical") + 1],
                                info[-1],
                                attribute).__dict__)



soup = card_page_init(str(sys.argv[1]))
card_url_list = card_urls(soup)

#Booster Set
card_url_list = card_url_list[1::3]
#Trial Deck
#card_url_list = card_url_list[1::4]

card_list = []

omit_list = ["/wiki/My_Buddy!"]

#Iterates through Card URLs in Set and Creates Card Objects
for url in card_url_list:
    if url not in omit_list:
        soup = card_page_init("https://buddyfight.fandom.com/" + url)
        card_create(soup, card_list)


#Opens/Creates json File and Dumps Card Objects
jsonFileName = str(sys.argv[1]).split('/')[-1].replace(":", "") + ".json"
with open("card_set_data/"+ jsonFileName, 'w') as f:
    json.dump(card_list, f, indent=4)

print("\n--Set Completed--\n")
