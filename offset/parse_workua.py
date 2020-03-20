import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

from utils import random_sleep, save_info

# global variables
HOST = 'https://www.work.ua'
ROOT_PATH = '/ru/jobs/'


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
            # get vacancy full info

        save_info(result)


if __name__ == "__main__":
    main()