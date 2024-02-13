import os
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

try:
    # NEW
    options = Options()
    options.add_argument('--no-sandbox')
    #options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get("https://steamdb.info/")
    bs = BeautifulSoup(driver.page_source, "html.parser")

    productsContainer = bs.find("div", {"class": "container-products"})
    productsRows = productsContainer.find_all("div", {"class": "row"})
    
    tablePopularReleases = productsRows[1].find("table", {"class": "table-products"})
    appRows = tablePopularReleases.find_all("tr", {"class": "app"})

    new = []

    for app in appRows:
        columns = app.find_all("td")
        name = columns[1].find("a", {"class": "css-truncate"}).get_text(strip=True)
        name = (name[:30] + '..') if len(name) > 30 else name
        peak = columns[2].get_text()
        price = columns[3].get_text()
        gameInfo = {"name": name, "peak": peak, "price": price}
        new.append(gameInfo)
    
    now = datetime.now()
    steamNew = '<span size="large" weight="bold" foreground="#B48EAD" stretch="expanded">NEW</span>\n'
    steamNew += '<span size="xx-small">\n</span>'
    for game in new:
        # color games based on peak
        peak = int(game['peak'].replace(',', ''))
        color = "#BF616A"
        if (peak >= 10000):
            color = "#A3BE8C"
        elif (peak >= 5000):
            color = "#8FBCBB"
        elif (peak >= 3000):
            color = "#EBCB8B"
        elif (peak >= 1000):
            color = "#D08770"
        steamNew += '<span weight="bold" foreground="' + color + '">' + game['name'] + '</span>'
        steamNew += '<span foreground="' + color + '"> | ' + game['peak'] + '</span>\n'

    outputFile = open(os.path.expanduser('~') + '/.config/eww/steam_new.txt', 'w+')
    outputFile.write(steamNew.replace('&', '&amp;'))
    outputFile.close()

    # TRENDING
    firstRowTables = productsRows[0].find_all("table", {"class": "table-products"})
    tableTrending = firstRowTables[1]
    appRows = tableTrending.find_all("tr", {"class": "app"})

    trendig = []

    for app in appRows:
        columns = app.find_all("td")
        name = columns[1].find("a", {"class": "css-truncate"}).get_text(strip=True)
        name = (name[:30] + '..') if len(name) > 30 else name
        
        try:
            players = columns[3].get_text()
        except:
            players = "0"
        
        gameInfo = {"name": name, "players": players}
        trendig.append(gameInfo)
    
    # Sort by players
    trendig = sorted(trendig, key=lambda x: int(x['players'].replace(',', '')), reverse=True)

    steamTrending = '<span size="large" weight="bold" foreground="#B48EAD" stretch="expanded">TRENDING</span>\n'
    steamTrending += '<span size="xx-small">\n</span>'
    for game in trendig:
        # color games based on peak
        players = int(game['players'].replace(',', ''))
        color = "#BF616A"
        if (players >= 10000):
            color = "#A3BE8C"
        elif (players >= 5000):
            color = "#8FBCBB"
        elif (players >= 3000):
            color = "#EBCB8B"
        elif (players >= 1000):
            color = "#D08770"
        steamTrending += '<span weight="bold" foreground="' + color + '">' + game['name'] + '</span>'
        steamTrending += '<span foreground="' + color + '"> | ' + game['players'] + '</span>\n'

    outputFile = open(os.path.expanduser('~') + '/.config/eww/steam_trending.txt', 'w+')
    outputFile.write(steamTrending.replace('&', '&amp;'))
    outputFile.close()

    # UPCOMING
    driver.get("https://steamdb.info/upcoming/?nosmall")
    bs = BeautifulSoup(driver.page_source, "html.parser")

    body = bs.find("div", {"class": "body-content"})
    releasesContainer = body.find("div", {"class": "container"}, recursive=False)

    releases = []

    # Get first 10 dates
    dates = releasesContainer.find_all("div", {"class": "pre-table-title"})
    releasesIndex = 0
    
    for date in dates:
        dateText = date.find("a").find_all(string=True, recursive=False)[-1].strip()
        dateObject = datetime.strptime(dateText, '%d %B %Y')
        formattedDate = dateObject.strftime('%d.%m.%Y')
        releases.append({"date": formattedDate, "games": []})
        releasesIndex = releasesIndex + 1;
        if releasesIndex >= 20:
            break;
    
    # Assign first 10 game lists to dates
    games = releasesContainer.find_all("div", {"class": "dataTables_wrapper"})
    releasesIndex = 0

    for game in games:
        appRows = game.find_all("tr", {"class": "app"})
        for app in appRows:
            gameInfo = {}
            name = app.find('a', {"class": "b"}).get_text(strip=True)
            name = (name[:30] + '..') if len(name) > 30 else name
            followers = app.find('td', {"class": "text-center"}).get_text(strip=True)            
            gameInfo = {"name": name, "followers": followers}
            releases[releasesIndex]["games"].append(gameInfo)
        
        # sort games by number of followers
        releases[releasesIndex]["games"] = sorted(releases[releasesIndex]["games"], key=lambda x: int(x['followers'].replace(',', '')), reverse=True)

        releasesIndex = releasesIndex + 1;
        if releasesIndex >= 20:
            break;
    
    releasesIndex = 0
    totalGamesPrinted = 0 # limit to 15 games

    # Print upcoming releases
    steamUpcoming = '<span size="large" weight="bold" foreground="#B48EAD" stretch="expanded">UPCOMING</span>\n'
    for releaseDay in releases:
        # Check if at least one game have more than 1000 followers
        if int(releaseDay['games'][0]['followers'].replace(',', '')) >= 1000:
            steamUpcoming += '<span size="xx-small">\n</span>'
            steamUpcoming += '<span size="large" weight="bold" foreground="#B48EAD">' + releaseDay['date'] + '</span>\n'
            for gameRelease in releaseDay['games']:
                followers = int(gameRelease['followers'].replace(',', ''))
                if followers >= 1000:
                    # color games based on followers
                    color = "#BF616A"
                    if (followers >= 20000):
                        color = "#A3BE8C"
                    elif (followers >= 10000):
                        color = "#8FBCBB"
                    elif (followers >= 5000):
                        color = "#EBCB8B"
                    elif (followers >= 3000):
                        color = "#D08770"
                    
                    steamUpcoming += '<span weight="bold" foreground="' + color + '">' + gameRelease['name'] + '</span>'
                    steamUpcoming += '<span foreground="' + color + '"> | ' + gameRelease['followers'] + '</span>\n'
                    
                    # limit to 15 printed games
                    totalGamesPrinted = totalGamesPrinted + 1
                    if totalGamesPrinted >= 15:
                        releasesIndex = 10
                        break;
            
        releasesIndex = releasesIndex + 1;
        if releasesIndex >= 10:
            break;
    
    now = datetime.now()
    steamUpcoming += '<span size="xx-small">\n</span>'
    steamUpcoming += '<span foreground="#B48EAD">(' + now.strftime("%d.%m.%Y %H:%M:%S") + ')</span>'
    
    outputFile = open(os.path.expanduser('~') + '/.config/eww/steam_upcoming.txt', 'w+')
    outputFile.write(steamUpcoming.replace('&', '&amp;'))
    outputFile.close()

finally:
    try:
        driver.quit()
    except:
        pass