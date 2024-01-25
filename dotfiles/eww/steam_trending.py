from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

try:
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless=new")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-data-dir=/home/rstasta/.cache/selenium-chrome")
    driver = webdriver.Chrome(options=options)
    driver.get("https://steam250.com/trending")
    bs = BeautifulSoup(driver.page_source, "html.parser")

    # Get all charts tables
    rankingMainDiv = bs.find("div", {"class": "col1 main ranking"})
    rankingDivs = rankingMainDiv.find_all(attrs={'id': True})
    games = []
    i = 0
    for rankingDiv in rankingDivs:
        gameDiv = rankingDiv.find("div", {"class": "appline"})
        if (gameDiv != None):
            name = gameDiv.find("span", {"class": "title"}).find("a").string
            release = gameDiv.find("span", {"class": "date"})["title"]
            tag = gameDiv.find("a", {"class": "tag"}).string
            
            price = 'Free'
            try:
                price = gameDiv.find("span", {"class": "price"}).string
            except:
                pass

            rating = rankingDiv.find("span", {"class": "rating"}).string.replace("rated ", "")

            games.append({'name': name, 'release': release, 'price': price, 'tag': tag, 'rating': rating});
            i = i + 1
            if (i >= 20):
                break;

    resultTrending = ""
    for game in games:
        resultTrending += '<span weight="bold" size="large">' + game['name'] +  '</span>'
        resultTrending += game['tag'] + ' | ' + game['price'] + ' | ' + game['release'] + ' | ' + game['rating'] + '\n'
    
    steamTrendingFile = open('steam_trending.txt', 'w+')
    steamTrendingFile.write(resultTrending)
    steamTrendingFile.close()

finally:
    try:
        driver.quit()
    except:
        pass