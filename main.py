# encoding: utf-8
from bs4 import BeautifulSoup
from requests import get
from time import sleep
import json

limit = 5

def save(content):
    with open('filmes.json','w',encoding='utf8') as cmd:
        json.dump(content,cmd,indent=3, ensure_ascii=False)
    print('> Saved')

def urlGet(url,listUrl=[]):
    print(f'> Acessando... {url}')
    html = get(url).text
    sleep(1)
    listUrl.append(url)
    return BeautifulSoup(html,'html.parser'),listUrl

def getData(pageLink):
    site,_ = urlGet(pageLink)
    magnets = site.find('p',attrs={'id':'lista_download'})
    data={
        'informações': site.find('div',attrs={'id':'informacoes'}).text,
        'magnet': magnets.findAll('a')[1].attrs['href']
    }
    return data

def getMovies(movies,listMovies):
    for movie in movies:
        name = movie.find("h3").text
        listMovies[name] = getData(movie.find('a').attrs['href'])
    return listMovies

def fetchMovies(site,listMovies):
    tableMovies = site.find('div',href=False,attrs={'id':'capas_pequenas'})
    movies = tableMovies.findAll('div',href=False,attrs={'class':'capa_larga align-middle'})
    return getMovies(movies,listMovies)

def validation(nextUrl,listUrl,defaultNumber):
    if nextUrl in listUrl:
        defaultNumber+=1
        return defaultNumber
    return None

def end(site):
    pagination = site.find('div',attrs={'class':'paginacao text-center'})
    numberCurrentPage =pagination.find('li',attrs={'class':'page-item active'}).text
    print(numberCurrentPage)
    if numberCurrentPage == str(limit):
        return True
    return False

def fetchAllPagesMovies():
    listUrl=[]
    movies={}
    site, listUrl= urlGet("https://viatorrents.com/5.1/1/",listUrl)
    pagination = site.find('div',attrs={'class':'paginacao text-center'})
    movies = fetchMovies(site, movies)
    defaultNextPage=2
    while(True):
        pagination = site.find('div',attrs={'class':'paginacao text-center'})
        nextPage = pagination.findAll('li')[defaultNextPage]
        url2 = nextPage.find('a').attrs['href']
        if end(site):
            break
        if not validation(url2,listUrl,defaultNextPage) == None:
            defaultNextPage= validation(url2,listUrl,defaultNextPage)
            continue
        movies = fetchMovies(site, movies)
        site,listUrl = urlGet(url2,listUrl)
        save(movies)
    return movies

def main():
    fetchAllPagesMovies()

if __name__ == "__main__":
    main()