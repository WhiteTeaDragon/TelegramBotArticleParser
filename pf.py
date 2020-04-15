import requests
from bs4 import BeautifulSoup
import urllib.parse
from variables import *

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET,
                               username=username, password_hash=password_hash, session_key=None)


vars = [('"', '"'), ('«', '»'), ('“', '”'), ('‘', '’')]


def get_text(url):
    rs = requests.get(url, headers=headers)
    if rs:
        html = BeautifulSoup(rs.text, 'html.parser')
        paragraphs = html.select("p")
        ans = ""
        for para in paragraphs:
            ans += para.text
        paragraphs = html.select("li")
        for para in paragraphs:
            ans += para.text
        return ans
    return None


def change_for_comp(str):
    ans = ""
    for i in range(len(str)):
        if str[i].isalpha():
            ans += str[i].lower()
    return ans


def check_song(song_name, session):
    search_results = pylast.TrackSearch(track_title=song_name, artist_name="", network=session)
    page = search_results.get_next_page()
    MAX = min(3, len(page))
    for i in range(MAX):
        if len(page) > i:
            res = page[i]
            art = res.artist
            tit = res.title
            if abs(len(tit) - len(song_name)) < 5 and (change_for_comp(tit)).find(change_for_comp(song_name)) != -1:
                return (True, art, tit)
    return (False, None, song_name)


def check_site(url):
    #url = 'https://pitchfork.com/reviews/albums/nils-frahm-all-melody/'
    #url = "https://pitchfork.com/reviews/albums/nils-frahm-all-encores/"
    #url = "https://pitchfork.com/reviews/albums/jonathan-fireeater-tremble-under-boom-lights/"
    #url = "https://pitchfork.com/reviews/tracks/lil-tjay-lil-baby-decline/"
    #url = "https://pitchfork.com/reviews/albums/floating-points-crush/"
    #url = "https://pitchfork.com/reviews/albums/jimmy-eat-world-surviving/"
    #url = "https://pitchfork.com/news/bad-bunny-joins-natanael-cano-on-new-soy-el-diablo-remix-listen/"
    #url = "https://pitchfork.com/news/kanye-wests-new-album-jesus-is-king-is-here-listen/"
    #url = "https://pitchfork.com/reviews/albums/relaxer-coconut-grove/"
    #url = "https://pitchfork.com/news/watch-billie-eilish-perform-bad-guy-and-i-love-you-on-snl/"
    #url = "https://en.wikipedia.org/wiki/Yuri_Shatunov"
    #url = "https://thequietus.com/articles/28104-melt-yourself-down-100-yes-review"
    #url = "https://www.caughtbytheriver.net/2020/04/country-music/"
    url = urllib.parse.unquote(url)
    try:
        content = get_text(url)
    except Exception:
        return "Проблемы с подключением к странице, возможно, в адресе опечатка."
    if content is None:
        return "К сожалению, я не могу подключиться к этой странице."
    names_set = set()
    pairs_set = set()
    ans = ""
    i = 0
    while i < len(content):
        flag = True
        for jj in range(len(vars)):
            if not flag:
                break
            if content[i] == vars[jj][0]:
                flag = False
                j = i + 1
                while j < len(content) and content[j] != vars[jj][1]:
                    j += 1
                curr = content[i + 1:j]
                if curr not in names_set:
                    flag, artist, song_name = check_song(curr, network)
                    names_set.add(song_name)
                    if flag and (artist, song_name) not in pairs_set:
                        ans += str(song_name) + " by " + str(artist) + '\n'
                        pairs_set.add((artist, song_name))
        i += 1
    return ans
