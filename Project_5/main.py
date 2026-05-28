import requests
from bs4 import BeautifulSoup
import time


headers = { # Заголовки для request запроса, чтобы сайт думал что мы браузерный запрос, а не из вне.
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',}



# Получение погоды в любом городе России(EN) путём скрапинга сайта
def get_weather(city: str, headers: any):
    response = requests.get(url=f'https://world-weather.ru/pogoda/russia/{city}/?ysclid=mfsi3cz4wt966294283', headers=headers)
    parser = BeautifulSoup(response.text, 'html.parser')
    print(f'Статус код: {response.status_code}.')
    if response.status_code == 200:
        weather_descript = parser.find(name='div', id='weather-now-description')
        l = weather_descript.find_all(name='dd')
        feels = l[0].text
        pressure = l[1].text
        humidity = l[2].text
        wind = l[3].text
        gusts_of_wind = l[4].text
        cloud_cover = l[5].text
        visibillity = l[6].text
        return (f'Ощущается:    {feels}\n'
                f'Давление:     {pressure}\n'
                f'Влажность:    {humidity}\n'
                f'Ветер:        {wind}\n'
                f'Порывы ветра: {gusts_of_wind}\n'
                f'Oблачность:   {cloud_cover}\n'
                f'Видимость:    {visibillity}')
    else:
        return response.status_code


# Получение новостей из интернета, путём скрапинга сайтов.
def get_news(headers: any):
    response = requests.get(url='https://ria.ru/', headers=headers)
    print(f'Status code: {response.status_code}')
    if response.status_code == 200:
        parser = BeautifulSoup(response.text, 'html.parser')
        news_list2 = parser.find_all('div', class_='cell-list__item m-no-image')
        l = [new.text for new in news_list2]
        s = '\n'.join(l)
        spliter = s.split('\n')
        l2 = [(s[0:-5], s[-5:]) for s in spliter]
        l3 = []
        m = 0
        for d in l2:
            l3.append(d)
            m+= 1
            if m == 5:
                break
        return (f'📌 1. {l3[0][0]}\nTime: {l3[0][1]}\n\n'
                f'📌 2. {l3[1][0]}\nTime: {l3[1][1]}\n\n'
                f'📌 3. {l3[2][0]}\nTime: {l3[2][1]}\n\n'
                f'📌 4. {l3[3][0]}\nTime: {l3[3][1]}\n\n'
                f'📌 5. {l3[4][0]}\nTime: {l3[4][1]}')

    else:
        return 'Data is None'



if __name__ == '__main__':
    print(get_news(headers=headers))
