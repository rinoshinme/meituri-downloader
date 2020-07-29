import os
import requests
from bs4 import BeautifulSoup
import time
import urllib


BASE_URL = 'https://www.rosi263.com'


def url_get_article_pages(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
    print(response.content.decode('utf-8'))
    try:
        divs = soup.find_all(name='div', attrs={'class': 'pagination2'})
        text = divs[0].text
        num_pages = int(text.split(':')[0][2:-1])

        urls = [url]
        base_add = url[:-5]
        for i in range(2, num_pages + 1):
            urls.append('{}_{}.html'.format(base_add, i))
        return urls
        
    except Exception as e:
        print('error: ' + str(e))
        return None


def url_get_download_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')

    article = soup.find(name='article', attrs={'class': 'article-content'})

    imgs = article.find_all('img')
    links = [img['src'] for img in imgs]
    links = [BASE_URL + l for l in links]
    return links


def download_article(article_url, folder):
    pages = url_get_article_pages(article_url)
    time.sleep(0.5)
    
    links = []
    for page in pages:
        ls = url_get_download_links(page)
        links.extend(ls)
        time.sleep(0.1)
    print('{} images for download'.format(len(links)))
    
    for link in links:
        filename = link.split('/')[-1]
        save_path = os.path.join(folder, filename)
        if os.path.exists(save_path):
            continue
        print('downloading [image] {}'.format(link))
        urllib.request.urlretrieve(link, save_path)
        time.sleep(0.5)


def url_get_articles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
    articles = soup.find_all(name='h2')
    article_links = [a.find('a')['href'] for a in articles]
    article_links = [BASE_URL + l for l in article_links]
    article_titles = [a.text for a in articles]

    return article_links, article_titles


def main():
    total_pages = 57
    main_urls = ['http://www.rosi263.com/rosi_mm/list_6_{}.html'.format(i) for i in range(1, total_pages + 1)]
    for main_url in main_urls:
        articles, titles = url_get_articles(main_url)
        for art, title in zip(articles, titles):
            save_folder = os.path.join('./rosimm', title)
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            print('downloading [article] {}'.format(art))
            download_article(art, save_folder)


if __name__ == '__main__':
    # main()
    url = 'https://www.rosi263.com/rosi_mm/3262.html'
    download_article(url, './rosimm')
