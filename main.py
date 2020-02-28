import requests
from bs4 import BeautifulSoup
import re
import csv
from os.path import isfile

def setup_csv(file_handle, writeheader=False):
    """
    Returns a CSV writer
    """
    headers = [
        "ID", "Name", "Year", "Season", 'English', 'Japanese', 'Episodes',
        'Broadcast', 'Source', 'Duration', 'Rating', 'Score', 'Members',
        'Favorites', 'Action', 'Adventure', 'Cars', 'Comedy', 'Dementia',
        'Demons', 'Drama', 'Ecchi', 'Fantasy', 'Game', 'Harem', 'Hentai',
        'Historical', 'Horror', 'Josei', 'Kids', 'Magic', 'Martial Arts',
        'Mecha', 'Military', 'Music', 'Mystery', 'Parody', 'Police',
        'Psychological', 'Romance', 'Samurai', 'School', 'Sci-Fi', 'Seinen',
        'Shoujo', 'Shoujo Ai', 'Shounen', 'Shounen Ai', 'Slice of Life',
        'Space', 'Sports', 'Super Power', 'Supernatural', 'Thriller',
        'Vampire', 'Yaoi', 'Yuri'
    ]
    writer = csv.DictWriter(file_handle, headers)
    if writeheader:
        writer.writeheader()
    return writer


def add_to_csv(csv, anime):
    """
    Add new entry in dataset
    """
    csv.writerow(anime)


def parse_duration(string):
    """
    Parses episode duration strings and returns number of minutes.
    For example:
        "3 hr. 2 min. 1 sec. per ep." -> 183
        "1 hr. 45 min." -> 105
        "23 min. per ep." -> 23
        "42 sec. per ep." -> 1
        "29 sec. per ep." -> 1
        "Unknown" -> None
        "N/A" -> None
    These examples prints error to stdout:
        "0 sec. per ep." -> None
        "???" -> None
    """
    def match_time(string, unit):
        match = re.search(f"\d+(?= {unit})", string)
        return int(match.group(0)) if match else 0
    seconds = match_time(string, "sec")
    minutes = 0 if seconds == 0 else 1
    minutes += match_time(string, "min")
    minutes += match_time(string, "hr") * 60
    if minutes == 0:
        if string != "Unknown" and string != "N/A":
            print(f"ERROR: '{string}' not a duration > 0 seconds")
        return
    return minutes


def parse_number(string):
    try:
        return int(string.replace(",", ""))
    except:
        try:
            return float(string)
        except:
            if string != "Unknown" and string != "N/A":
                print(f"ERROR: {string} not number")
            return


def parse_anime(soup):
    """
    Return anime information extracted from the given soup.

    Specifically, anime name; year; season; and all data from the “Information” (except for “Type”--since all animes we analyze are of type TV--and “Status”), “Statistics,” “Summary Stats,” and “Score Stats” section 

    For example: {
        "English":"Interspecies Reviewers",
        "Japanese":"異種族レビュアーズ",
        "Episodes":12,
        "Broadcast":"Saturdays at 23:00 (JST)",
        "Source":"Manga",
        "Ecchi":1,
        "Fantasy":1,
        "Comedy":1,
        "Duration":23,
        "Rating":"R+ - Mild Nudity",
        "Score":7.61,
        "Members":168268,
        "Favorites":17542
    }
    """
    info = [
        div.stripped_strings for div in 
        soup.find("h2", text="Alternative Titles").find_next_siblings("div")
    ]
    name = next(soup.find("span", itemprop="name").strings)
    result = { 'Name': name }
    ignored_keys = {
        "Synonyms", "Type", "Status", "Aired", "Premiered",
        "Producers", "Licensors", "Studios", "Popularity", "Ranked"
    }
    to_number_keys = {
        "Episodes", "Score", "Members", "Favorites"
    }
    for generator in info:
        try:
            key = next(generator).rstrip(':')
            if key not in ignored_keys:
                if key in to_number_keys:
                    result[key] = parse_number(next(generator))
                elif key == 'Genres':
                    result.update({ genre: 1 for genre in set(generator) if genre != ',' })
                elif key == 'Duration':
                    result['Duration'] = parse_duration(next(generator))
                else:
                    result[key] = next(generator)
        except StopIteration:
            pass
    return result


def get_anime(url):
    """
    Download and parse {url}/stats
    """
    components = url.split('/')
    anime_id = components[4]
    name = re.sub('_+', ' ', components[-1])
    print(f"Processing {anime_id}: {name}")

    html = requests.get(f"{url}/stats").text
    soup = BeautifulSoup(html, 'html.parser')
    return { **parse_anime(soup), "ID": anime_id, "Name": name }


def parse_season(soup):
    """
    Returns a list of urls for all new animes of the given season soup
    """
    return [
        # Get url for each href from all inner `a` tags with class="link-title"
        link["href"] for link in 
        # Find the first `div` with class="... js-seasonal-anime-list-key-1 ..." 
        soup.find("div", class_="js-seasonal-anime-list-key-1") \
            .find_all("a", class_="link-title")
    ]


def get_season(csv, year, season):
    season_url = f"https://myanimelist.net/anime/season/{year}/{season}"
    html = requests.get(season_url).text
    soup = BeautifulSoup(html, 'html.parser')
    for anime_url in parse_season(soup):
        add_to_csv(csv, {
            **get_anime(anime_url),
            "Year": year,
            "Season": season
        })


def get_year(csv, year):
    for season in reversed(["winter", "spring", "summer", "fall"]):
        get_season(csv, year, season)


def get_all_years(csv, start=2020, end=1916):
    for year in range(start, end, -1 if start > end else 1):
        get_year(csv, year)


OUTPUT = 'sample.csv'


def main():
    file_exists = isfile(OUTPUT)
    with open(OUTPUT, 'a+') as f:
        csv = setup_csv(f, writeheader=not file_exists)
        # get_year(csv, 2019)
        # get_all_years(csv, end=2018)


if __name__ == "__main__":
    main()
