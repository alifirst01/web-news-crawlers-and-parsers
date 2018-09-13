import os
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import queue
import cfscrape
from Scripts.parse_dawn import processArticleHtml

def fetch_proxies():
    scraper = cfscrape.create_scraper()
    proxies = []
    PROXY_URLS = ["https://hidemy.name/en/proxy-list/"]
    for url in PROXY_URLS:
        success = False
        while not success:
            try:
                random_agent = global_ua.random
                headers = {'User-Agent': random_agent}
                soup = BeautifulSoup(scraper.get(url, headers=headers).text, "html.parser")
                for row in soup.findAll('table')[0].tbody.findAll('tr'):
                    columns = row.findAll('td')
                    ip = columns[0].contents[0]
                    port = columns[1].contents[0]
                    ping = int(row.findAll('p')[0].contents[0].split(" ")[0])
                    protocol = columns[4].contents[0].split(',')[0].lower()
                    proxies.append((ip, port, ping, protocol))
                success = True
            except Exception as ex:
                print(ex)
                print('Cannot get proxy')
                success = False
    filtered_proxies = [p for p in proxies if p[3] in ["http", "https"]]
    return filtered_proxies


def refresh_proxy_queue():
    global proxy_queue
    proxies = fetch_proxies()
    for proxy in proxies:
        proxy_queue.put(proxy)


def getTodayUrls():
    retry = 3
    urls = []
    while True:
        try:
            url = 'https://www.dawn.com/latest-news'
            proxy = proxy_queue.get()
            random_agent = global_ua.random
            headers = {'User-Agent': random_agent}
            proxies = {proxy[3]: "{0}://{1}:{2}".format(proxy[3], proxy[0], proxy[1])}
            response = requests.get(url, timeout=10, headers=headers, proxies=proxies)
            status = response.status_code
            res_text = response.text
            urls = []
            if status == 200:
                soup = BeautifulSoup(res_text, 'html.parser')
                container = soup.find('div', {'class': 'content'})
                articles = container.find_all('article')
                for article in articles:
                    urls.append(article.find('a')['href'])
            break
        except:
            if retry == 0:
                break
            retry -= 1
    return urls


def worker():
    print('Dawn Thread Starting')
    Parent_DIR = os.getcwd()
    DIR = os.path.join(Parent_DIR, 'Htmls', 'Dawn_HtmlFiles')
    LOG_DIR = os.path.join(Parent_DIR, 'Logs')

    if not os.path.exists(DIR):
        os.mkdir(DIR)
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)

    logs = open(os.path.join(LOG_DIR, 'dawn_log.txt'), 'a')
    processed = [x.split('.')[0] for x in os.listdir(DIR)]

    global proxy_queue, global_ua
    global_ua = UserAgent()
    proxy_queue = queue.Queue()

    refresh_proxy_queue()
    urls = getTodayUrls()

    for url in urls:
        if url.split('/')[-1] in processed:
            continue
        retry = 1
        while retry >= 0:
            try:
                random_agent = global_ua.random
                if proxy_queue.empty():
                    refresh_proxy_queue()
                proxy = proxy_queue.get()
                headers = {'User-Agent': random_agent}
                proxies = {proxy[3]: "{0}://{1}:{2}".format(proxy[3], proxy[0], proxy[1])}
                response = requests.get(url, timeout=10, headers=headers, proxies=proxies)
                status = response.status_code
                res_text = response.text

                if status == 200:
                    directory = os.getcwd()
                    filename = url.split('/')[-1] + '.html'
                    path = os.path.join(str(directory), DIR, filename)
                    f = open(path, 'w', encoding='utf-8')
                    f.write(res_text)
                    f.close()
                    proxy_queue.put(proxy)
                    processArticleHtml(filename, url, logs)
                    print('Dawn: Article', url.split('/')[-1],'Saved')
                retry = -1

            except Exception as e:
                if retry == 0:
                    print('Dawn: Error in processing')
                    logs.write('Error in processing ' + ': ' + str(e) + '\n')
                    logs.flush()
                retry -= 1