# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


def parse_tiobe(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    header = soup.find('h2')
    name = header.find('b').getText()
    results = soup.find(id='top20')
    tbody = results.find('tbody')
    table_data = tbody.find_all("tr")

    languages = []
    ratings = []

    for elem in table_data:
        td_elem = elem.find_all('td')
        languages.append(td_elem[3].getText())
        ratings.append(float(td_elem[4].getText()[:-1]))

    total = 0.0

    for rating in ratings:
        total = total + rating

    ratings.append(round((100.00 - total), 2))

    print()
    print(name + ' (' + url + ')')

    for i in range(0, 20):
        print(str(i + 1) + '. ' + languages[i] + ' (' + str(ratings[i]) + '%)')


def parse_pypl(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    header = soup.find('h1').getText()
    # subhead = soup.find(id='countryDate').getText()
    script = soup.find('script')
    tags = script.prettify().split('<td>')

    languages = []
    ratings = []

    for i in range(1, 21):
        parts = tags[i].split('</td><td class=right>')
        languages.append(parts[0])
        ratings.append(float(parts[1].split(' %')[0]))

    languages.append('All Others')

    total = 0.0

    for rating in ratings:
        total = total + rating

    ratings.append(round((100.00 - total), 2))

    print()
    print(header + ' (' + url + ')')

    for i in range(0, 20):
        print(str(i + 1) + '. ' + languages[i] + ' (' + str(ratings[i]) + '%)')


def parse_dbengines(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    header = soup.find('h1').getText()

    start = page.text.index("<table class=dbi>")
    end = page.text.index("</table>", start)
    table_data = page.text[start: end: 1]
    split_data = table_data.split('<th class="pad-l">')

    languages = []
    ratings = []

    for i in range(1, 21):
        split_parts = split_data[i].split('<td class="pad-l">')
        languages.append(split_parts[0].split(">")[1].split("<")[0].strip())
        ratings.append(float(split_parts[1].split("<")[0]))

    print()
    print(header + ' (' + url + ')')

    for i in range(0, 20):
        print(str(i + 1) + '. ' + languages[i] + ' (' + str(ratings[i]) + ')')


parse_tiobe('https://www.tiobe.com/tiobe-index/')
parse_pypl('http://pypl.github.io/PYPL.html')
parse_pypl('http://pypl.github.io/IDE.html')
parse_pypl('http://pypl.github.io/ODE.html')
parse_pypl('http://pypl.github.io/DB.html')
parse_dbengines('https://db-engines.com/en/ranking')
