import sqlite3

import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

from utils import random_sleep, save_info


db = sqlite3.connect('workua.sqlite')
cur = db.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS jobs (
            workua_id INTEGER NOT NULL,
            vacancy TEXT NOT NULL,
            company TEXT NOT NULL,
            address TEXT,
            salary TEXT)'''
            )

# global variables
HOST = 'https://www.work.ua'
ROOT_PATH = '/jobs/'


def main():
    page = 0

    while True:
        page += 1

        payload = {
            'ss': 1,
            'page': page,
        }

        user_agent = generate_user_agent()
        headers = {
            'User-Agent': user_agent,
        }

        print(f'PAGE: {page}')
        response = requests.get(HOST + ROOT_PATH, params=payload, headers=headers)
        response.raise_for_status()
        random_sleep()

        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        class_ = 'card card-hover card-visited wordwrap job-link'
        cards = soup.find_all('div', class_=class_)
        if not cards:
            cards = soup.find_all('div', class_=class_ + ' js-hot-block')

        result = []
        if not cards:
            break

        for card in cards:
            tag_a = card.find('h2').find('a')
            title = tag_a.text
            href = tag_a['href']
            result.append([title, href])
            vac_response = requests.get(HOST + href, headers=headers)
            vac_html = vac_response.text
            vac_soup = BeautifulSoup(vac_html, 'html.parser')

            workua_id = int(href.split('/')[-2])

            vacancy = vac_soup.find('h1', id='h1-name').text

            address = vac_soup.find('p', class_='text-indent add-top-sm').text.strip()
            address = address.split('\n')[0]

            blocks = vac_soup.find_all('p', class_='text-indent text-muted add-top-sm')
            for block in blocks:
                if block.find('a') is not None:
                    company = block.find('a').find('b').text
                else:
                    if block.find('b') is not None:
                        salary = block.find('b').text
                        salary = salary.replace('\u202f', '')
                        salary = salary.replace('\u2009', '')
                if not 'salary' in locals():
                    salary = None

            data = (workua_id, vacancy, company, address, salary)
            cur.execute('''INSERT INTO jobs VALUES (?, ?, ?, ?, ?)''', data)

            db.commit()

        save_info(result)

    db.close()

if __name__ == "__main__":
    main()
