import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

try:
    #TRENDING
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless=new")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.get("https://steam250.com/trending")
    bs = BeautifulSoup(driver.page_source, "html.parser")

    rankingMainDiv = bs.find("div", {"class": "col1 main ranking"})
    rankingDivs = rankingMainDiv.find_all(attrs={'id': True})
    games = []
    i = 0
    for rankingDiv in rankingDivs:
        gameDiv = rankingDiv.find("div", {"class": "appline"})
        if (gameDiv != None):
            name = gameDiv.find("span", {"class": "title"}).find("a").string
            name = (name[:40] + '..') if len(name) > 40 else name
            tag = gameDiv.find("a", {"class": "tag"}).string
            
            price = 'Free'
            try:
                price = gameDiv.find("span", {"class": "price"}).string
            except:
                pass

            rating = rankingDiv.find("span", {"class": "rating"}).string.replace("rated ", "")
            velocity = rankingDiv.find("span", {"class": "velocity"}).get_text(strip=True).replace("velocity", "")

            games.append({'name': name, 'velocity': velocity, 'price': price, 'tag': tag, 'rating': rating});
            i = i + 1
            if (i >= 20):
                break;

    now = datetime.now()

    resultTrending = '<span size="large" weight="bold" foreground="#B48EAD" stretch="expanded" rise="10pt">STEAM TRENDING (' + now.strftime("%d.%m.%Y %H:%M:%S") + ')</span>\n'
    for game in games:
        ratingNumber = int(game['rating'].replace('%',''))
        color = "#BF616A"
        if (ratingNumber >= 50):
            color = "#D08770"
        if (ratingNumber >= 70):
            color = "#EBCB8B"
        if (ratingNumber >= 80):
            color = "#8FBCBB"
        if (ratingNumber >= 90):
            color = "#A3BE8C"
        resultTrending += '<span foreground="' + color + '" weight="bold" size="large">' + game['name'] +  '</span> '
        
        resultTrending += game['tag'] + ' | ' + game['price'] + ' | ' + game['velocity'] + '\n'

    #NEW
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless=new")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.get("https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998&os=win&supportedlang=english&filter=popularnew&ndl=1")
    bs = BeautifulSoup(driver.page_source, "html.parser")

    resultsDiv = bs.find('div', {'id': 'search_resultsRows'})
    resultRows = resultsDiv.find_all('a', {'class': 'search_result_row'})
   
    games = []
    i = 0
    for resultRow in resultRows:
        name = resultRow.find('span', {'class': 'title'}).string
        name = (name[:40] + '..') if len(name) > 40 else name
        release = resultRow.find('div', {'class': 'search_released'}).string.strip().replace(',', '')
        reviews = resultRow.find('span', {'class': 'search_review_summary positive'})['data-tooltip-html']
        price = resultRow.find('div', {'class': 'discount_final_price'}).string

        reviewsSecondPart = reviews.split('<br>')[1]
        percentage = re.search(r'(\d+%)', reviewsSecondPart).group(1)
        reviews = re.search(r'(\d+) user reviews', reviewsSecondPart).group(1)
        reviews = f"{percentage} ({reviews} reviews)"
        percentage = int(percentage.replace('%',''))

        game = {'name': name, 'release': release, 'reviews': reviews, 'percentage': percentage, 'price': price}
        games.append(game)

        i = i + 1
        if (i >= 20):
            break

    now = datetime.now()

    resultNew = '<span size="large" weight="bold" foreground="#B48EAD" stretch="expanded" rise="10pt">STEAM NEW (' + now.strftime("%d.%m.%Y %H:%M:%S") + ')</span>\n'
    for game in games:
        ratingNumber = game['percentage']
        color = "#BF616A"
        if (ratingNumber >= 50):
            color = "#D08770"
        if (ratingNumber >= 70):
            color = "#EBCB8B"
        if (ratingNumber >= 80):
            color = "#8FBCBB"
        if (ratingNumber >= 90):
            color = "#A3BE8C"
        resultNew += '<span foreground="' + color + '" weight="bold" size="large">' + game['name'] +  '</span> '
        resultNew += game['reviews'] + ' | ' + game['price'] + '\n'
    
    result = resultTrending
    result += '\n'
    result += resultNew
    
    steamTrendingFile = open(os.path.expanduser('~') + '/.config/eww/steam_charts.txt', 'w+')
    steamTrendingFile.write(result)
    steamTrendingFile.close()

finally:
    try:
        driver.quit()
    except:
        pass