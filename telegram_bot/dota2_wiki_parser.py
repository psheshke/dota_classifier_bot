import requests
from bs4 import BeautifulSoup as bs
from hero_dict_url import url_dict

def parser(hero):

    hero = str(hero)


    url = 'https://dota2.gamepedia.com/' + hero.replace(' ', '_')

    session = requests.Session()
    request = session.get(url,)

    if request.status_code == 200:

        soup = bs(request.content, 'html.parser')
        div = soup.find_all('div', attrs={'class': 'mw-parser-output'})

        hero_text = div[0].find_all('p', )[0].getText()

        result = hero_text

        table = div[0].find_all('table', attrs={'class': 'infobox'})[0]

        img_url = table.find_all('td', )[0].a.img['src']

        heroBio = div[0].find_all('div', attrs={'id': 'heroBio'})[0]

        audio_url = heroBio.find_all('div')[1].audio.source['src']

    else:
        result = 'Что-то dotawiki недоступна, \n' \
                 'давай попробуем в другой раз поискать?'

        img_url = ''
        audio_url = ''
        print(request.status_code)

    d2ru = 'https://dota2.ru/heroes/' + url_dict[hero]

    session = requests.Session()
    request = session.get(d2ru, )

    if request.status_code == 200:

        soup = bs(request.content, 'html.parser')

        result = soup.find_all('div', attrs={'class': 'bio'})[0].find_all('p', )[0].getText()

    return result, img_url, audio_url