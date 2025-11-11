import requests
from bs4 import BeautifulSoup
import pandas as pd

titles = []
prices = []
availabilities = []
ratings = []
base_url = "https://books.toscrape.com/catalogue/page-{}.html"

for page in range(1, 51):
    url = base_url.format(page)
    res = requests.get(url)
    if res.status_code != 200:
        break
    soup = BeautifulSoup(res.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    for book in books:
        titles.append(book.h3.a['title'])
        prices.append(book.find('p', class_='price_color').text)
        availabilities.append(book.find('p', class_='instock availability').text.strip())
        ratings.append(book.p['class'][1])

df = pd.DataFrame({
    'Title': titles,
    'Price': prices,
    'Availability': availabilities,
    'Star Rating': ratings
})
df.to_csv('books.csv', index=False)


from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://www.imdb.com/chart/top/")
time.sleep(3)

movies = driver.find_elements(By.CSS_SELECTOR, 'li.ipc-metadata-list-summary-item')
ranks, titles, years, ratings = [], [], [], []

for movie in movies:
    rank = movie.find_element(By.CSS_SELECTOR, '.ipc-title__text').text.split('.')[0]
    title = movie.find_element(By.CSS_SELECTOR, '.ipc-title__text').text.split('. ')[1]
    year = movie.find_element(By.CSS_SELECTOR, '.cli-title-metadata-item').text
    rating = movie.find_element(By.CSS_SELECTOR, '.ipc-rating-star--rating').text
    ranks.append(rank)
    titles.append(title)
    years.append(year)
    ratings.append(rating)

df = pd.DataFrame({
    'Rank': ranks,
    'Movie Title': titles,
    'Year of Release': years,
    'IMDB Rating': ratings
})
df.to_csv('imdb_top250.csv', index=False)
driver.quit()


url = "https://www.timeanddate.com/weather/"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

cities, temps, conditions = [], [], []
rows = soup.select('table.zebra.tb-wt fw va-m tr')

for row in soup.select('table.zebra.tb-wt tbody tr'):
    cols = row.find_all('td')
    if len(cols) >= 3:
        cities.append(cols[0].text.strip())
        temps.append(cols[1].text.strip())
        conditions.append(cols[2].text.strip())

df = pd.DataFrame({
    'City Name': cities,
    'Temperature': temps,
    'Weather Condition': conditions
})
df.to_csv('weather.csv', index=False)
