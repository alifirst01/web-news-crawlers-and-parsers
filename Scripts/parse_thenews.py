import os
import re
import json
from bs4 import BeautifulSoup


def getID(file):
    id = file.split("-")[0]
    return id


def getURL(soup, id):
    url_address = 'https://www.thenews.com.pk/latest/'
    url = soup.link['href']
    if url == None:
        url = url_address + id
    return url


def getPublishedDate(soup):
    try:
        date = re.findall('[a-zA-Z0-9]+', soup.find('div', {"class": "category-date"}).string)
        date = date[0] + ' ' +  date[1] + ',' + date[2]
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
        author = re.findall('[a-zA-Z0-9]+', soup.find('div', {"class": "category-source"}).text)
        author = ' '.join(author)
    except:
        author = "None"
    return author


def getArticleText(soup):
    try:
        text = soup.find('div', {"class": "story-detail"}).text
        text = text.replace("googletag.cmd.push(function () {", '')
        text = text.replace("googletag.display('div-gpt-ad-rectangle_belowpost_btf');", '')
        text = text.replace("googletag.display", '')
        text = text.replace("});", '')
        text = text.replace('Advertisement', '')
        text = text.replace('\n\n\n\n','')

    except:
        text = "None"
    return text


def getTitle(soup, url):
    try:
        title = soup.title.text.split("|")[0]
    except:
        try:
            title = url.split("/")[-1]
        except:
            title = "None"
    return title


def writeJson(Json_DIR, articleId, title, url, published, text, author):
    sourceName = 'The News'
    dataDict = {'id': articleId, 'title': title, 'author': author, 'url': url, 'sourceName': sourceName,
                'published': published, 'body' : text}
    jsonData = json.dumps(dataDict)
    with open(os.path.join(Json_DIR, str(articleId) + str('.json')), 'w', encoding='utf-8') as outfile:
        json.dump(dataDict, outfile)



def processArticleHtml(file, url, log_file):
    Parent_DIR = os.getcwd()
    Html_Folder = os.path.join(Parent_DIR, 'Htmls', 'TheNews_HtmlFiles')
    Json_DIR = os.path.join(Parent_DIR, 'Jsons', 'TheNews_JsonFiles')
    if not os.path.exists(Json_DIR):
        os.mkdir(Json_DIR)

    retry = 3
    while retry:
        try:
            file_path = os.path.join(Html_Folder, file)
            soup = BeautifulSoup(open(file_path, 'r', encoding='utf8'), 'html.parser')

            article_id = getID(file)
            title = getTitle(soup, url)
            published = getPublishedDate(soup)
            author = getAuthor(soup)
            text = getArticleText(soup)

            writeJson(Json_DIR, article_id, title, url, published, text, author)
            retry = 0
        except Exception as e:
            retry -= 1
            if retry == 0:
                print("TheNews: Error Processing Json File " + str(article_id))
                log_file.write("Error Processing Json File " + str(article_id) + ": " + str(e) + '\n')
                log_file.flush()

