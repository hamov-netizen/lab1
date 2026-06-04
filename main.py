import requests
from bs4 import BeautifulSoup
import re


def parse_weather():
    url = 'https://world-weather.ru/pogoda/russia/omsk/february-2026/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    page = requests.get(url, headers=headers)
    print(f'Статус ответа: {page.status_code}')

    if page.status_code != 200:
        print('Ошибка загрузки страницы')
        return

    soup = BeautifulSoup(page.text, 'html.parser')

    month_block = soup.find('ul', class_='ww-month')

    if not month_block:
        print('Не удалось найти блок с погодой')
        return

    days = month_block.find_all('li', class_=re.compile(r'ww-month-weekend|ww-month-weekdays'))

    results = []

    for day in days:
        link = day.find('a')
        if not link:
            continue

        date_div = link.find('div')
        if not date_div:
            continue
        day_number = date_div.text.strip()

        temp_span = link.find('span')
        if temp_span:
            day_temp = temp_span.text.strip()
        else:
            day_temp = 'Нет данных'

        night_temp_span = link.find('p', class_='ww-month-i-box')
        if night_temp_span:
            night_temp = night_temp_span.text.strip()
        else:
            night_temp = 'Нет данных'

        weather_icon = link.find('i', class_=re.compile(r'icon-weather'))
        if weather_icon:
            weather_desc = weather_icon.get('title', 'Нет данных')
        else:
            weather_desc = 'Нет данных'

        results.append({
            'date': f'{day_number} февраля',
            'day_temp': day_temp,
            'night_temp': night_temp,
            'description': weather_desc
        })

    # Сохраняем результаты в файл
    with open('omsk_weather_feb2026.txt', 'w', encoding='utf-8') as f:
        f.write('Погода в Омске за февраль 2026 года:\n')
        f.write('=' * 50 + '\n\n')

        for item in results:
            f.write(f"{item['date']}:\n")
            f.write(f"  Днём: {item['day_temp']}\n")
            f.write(f"  Ночью: {item['night_temp']}\n")
            f.write(f"  Описание: {item['description']}\n")
            f.write('-' * 40 + '\n')

    print(f'Сохранено {len(results)} записей в файл omsk_weather_feb2026.txt')


    return results

if __name__ == '__main__':
    parse_weather()