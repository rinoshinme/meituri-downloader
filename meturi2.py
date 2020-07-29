import os
import requests
from bs4 import BeautifulSoup
import time
import urllib


DATA_DIR = './albums'
# URL = 'http://ii.hywly.com/a/1/{}/{}.jpg'
URL = 'https://lns.hywly.com/a/1/{}/{}.jpg'


def get_opener():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')]
    urllib.request.install_opener(opener)


def get_num_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
    items = soup.select('title')
    title = items[0].text
    # print(title)
    # if title.endswith('_图集谷'):
    #     title = title[:-4]
    title = '_'.join(title.split('_')[:-1])  # ignore _tujigu at last
    title = title.replace('/', '_')
    parts = title.split('[')
    nimages = int(parts[-1][:-2])
    return title, nimages


def download_images(links, folder, step_time=5):
    total_time = 0
    total_pauses = 0
    get_opener()
    for n, link in enumerate(links):
        name = link.split('/')[-1]
        start = time.time()
        target_path = os.path.join(folder, name)
        # ignore downloaded files
        if os.path.exists(target_path):
            continue
            
        print('Downloading %s' % link)
        urllib.request.urlretrieve(link, target_path)
        end = time.time()
        passed = end - start
        total_time += passed
        # print('Complete. Took %.2f seconds.' % passed)

        if passed < step_time:
            add = step_time - passed
            # print('Waiting for an additional %.2f seconds.' % add)
            time.sleep(add)
            total_pauses += add


def download_index(idx):
    url = 'https://www.tujigu.com/a/{}/'.format(idx)
    try:
        title, nimages = get_num_images(url)
        print('downloading {}'.format(title))
        if nimages == 0:
            return
        links = [URL.format(idx, k) for k in range(1, nimages + 1)]
        folder = os.path.join(DATA_DIR, '{:06d}_{}'.format(idx, title))
        if not os.path.exists(folder):
            os.makedirs(folder)
        download_images(links, folder, step_time=1.5)
    except Exception as e:
        print('error: ' + str(e))


def main(indices):
    templ = 'https://www.tujigu.com/a/{}/'
    for idx in indices:
        download_index(idx)


def get_indices(main_url):
    # main_url = 'https://www.tujigu.com/riben/2.html'
    resp = requests.get(main_url)
    text = resp.content.decode('utf-8')
    soup = BeautifulSoup(resp.content.decode('utf-8'), 'html.parser')
    ps = soup.select('li')

    indices = []
    for p in ps:
        url = p.a['href']
        if url.endswith('/'):
            url = url[:-1]
        parts = url.split('/')
        if parts[-2] == 'a':
            # print(parts[-1])
            idx = int(parts[-1])
            indices.append(idx)
    return indices



if __name__ == '__main__':
    # main()
    # get_indices()
    npages = 100
    # main_urls = ['https://www.tujigu.com/riben/'] + ['https://www.tujigu.com/riben/{}.html'.format(i) for i in range(npages)]
    main_urls = ['https://www.tujigu.com/riben/{}.html'.format(i) for i in range(2, npages)]
    for main_url in main_urls:
        print('getting indices for page {}'.format(main_url))
        indices = get_indices(main_url)
        main(indices)
