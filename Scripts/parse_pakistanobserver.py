import os
import json
from bs4 import BeautifulSoup


def getID(url):
    id = url.split("/")[-2]
    return id


def getPublishedDate(soup):
    try:
        date = soup.find('time',{'class','entry-date'})['datetime']
        date = date.split('T')
        date = date[0] + ' ' + date[1].split('+')[0]
    except:
        date = "None"
    return date


def getClearText(text):
    text = text.split(">")[1].strip('\n')
    while text[-1] == '\n' or text[-1] == ' ':
        text = text[:len(text) - 1]
    while text[0] == '\n' or text[0] == ' ':
        text = text[1:]
    text = text.replace('http://','')
    text = text.replace('https://', '')
    text = text.replace('.com', '')
    return text


def getAuthor(soup):
    try:
        author = soup.find('div', {'class':'td-post-author-name'}).text.split('By ')[1].split(' -')[0]
    except:
        author = "None"
    return author


def getArticleText(soup):
    try:
        text = soup.find('div', {"class": "td-post-content"}).text
    except:
        text = "None"
    return text


def getTitle(soup):
    title = soup.find('header',{'class':'td-post-title'}).find('h1').text
    return title


def writeJson(Json_DIR, articleId, title, url, published, text, author):
    sourceName = 'Pakistan Observer'
    dataDict = {'id': articleId, 'title': title, 'author': author, 'url': url, 'sourceName': sourceName,
                'published': published, 'body' : text}
    with open(os.path.join(Json_DIR, str(articleId) + str('.json')), 'w', encoding='utf-8') as outfile:
        json.dump(dataDict, outfile)



def processArticleHtml(file, url, log_file):
    Parent_DIR = os.getcwd()
    Html_Folder = os.path.join(Parent_DIR, 'Htmls', 'PakistanObserver_HtmlFiles')
    Json_DIR = os.path.join(Parent_DIR, 'Jsons', 'PakistanObserver_JsonFiles')
    if not os.path.exists(Json_DIR):
        os.mkdir(Json_DIR)

    retry = 3
    while retry:
        try:
            file_path = os.path.join(Html_Folder, file)
            soup = BeautifulSoup(open(file_path, 'r', encoding='utf8'), 'html.parser')

            article_id = getID(url)
            title = getTitle(soup)
            published = getPublishedDate(soup)
            author = getAuthor(soup)
            text = getArticleText(soup)

            writeJson(Json_DIR, article_id, title, url, published, text, author)
            retry = 0
        except Exception as e:
            retry -= 1
            if retry == 0:
                print("Pakistan Observer: Error Processing Json File " + str(article_id))
                log_file.write("Error Processing Json File " + str(article_id) + ": " + str(e) + '\n')
                log_file.flush()