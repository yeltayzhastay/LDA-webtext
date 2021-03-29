# https://kaz.tengrinews.kz/accidents/page/8/
import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

class parsing:
    def __init__(self, path='exp.csv', count=1):
        self.page_url = 'https://kaz.tengrinews.kz'
        result = []
        for url in list(set(self.__get_urls_posts(count))):
            result.append(self.__get_places_information(url))
            # sleep(0.2)
        pd.DataFrame(result, columns=['url', 'title', 'text']).to_csv(path, index=False)
        print('Successfully parsed and saved!')
 
    def __get_urls_posts(self, count=1):
        results = []
        for i in range(1, count):
            page = requests.get(self.page_url + '/accidents/page/' + str(i) + '/')
            soup = BeautifulSoup(page.content, 'html.parser')
            soup_find = soup.find_all(class_='tn-article-grid')[0]
            for job_elem in soup_find.find_all('a'):
                title_elem = job_elem.get('href')
                results.append(self.page_url + title_elem)
            # sleep(0.2)
        return results

    def __get_places_information(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find(class_='tn-content-title').text.split('\n')[0]
        text = soup.find(class_='tn-news-text').text[:-36]
        return [url, title, text]

if __name__ == '__main__':
    parse = parsing('dataset/tengri.csv', 100)