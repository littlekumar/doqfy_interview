from django.shortcuts import render
from .models import Nifty50Data
import requests
from bs4 import BeautifulSoup
import schedule
import time
import threading

def scrape_nifty50():
    url = 'https://www.nseindia.com/'
    headers = {
    }    
    response = requests.get(url, headers=headers)
    print('---14---',response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'table-striped'})
    rows = table.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        symbol = cols[0].text.strip()
        name = cols[1].text.strip()
        price = cols[2].text.strip()
        change = cols[3].text.strip()
        percent_change = cols[4].text.strip()
        Nifty50Data.objects.create(
            symbol=symbol,
            name=name,
            price=price,
            change=change,
            percent_change=percent_change
        )

def schedule_scraping():
    print('----31---')
    # scrape_nifty50()
    schedule.every(5).minutes.do(scrape_nifty50())
    while True:
        schedule.run_pending()
        time.sleep(1)

thread = threading.Thread(target=schedule_scraping)
thread.daemon = True
thread.start()

def index(request):
    data = Nifty50Data.objects.all()
    return render(request, 'index.html', {'data': data})

