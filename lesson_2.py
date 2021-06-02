import typing
import requests
from urllib.parse import urljoin
import bs4
import time
import pymongo
from datetime import datetime


class GbBlogParse:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) "
        "Gecko/20100101 Firefox/88.0"
    }
    __parse_time = 0

    def __init__(self, start_url, db, delay=1.0):
        self.start_url = start_url
        self.db = db
        self.delay = delay
        self.done_url: typing.Set[str] = set()
        self.tasks: typing.List[typing.Callable] = []
        self.task_creator({self.start_url,}, self.parse_feed)

    def _get_response(self, url):
        while True:
            next_time = self.__parse_time + self.delay
            if next_time > time.time():
                time.sleep(next_time - time.time())
            response = requests.get(url, headers=self.headers)
            print(f"RESPONSE: {response.url}")
            self.__parse_time = time.time()
            if response.status_code == 200:
                return response

    def get_task(self, url: str, callback: typing.Callable) -> typing.Callable:
        def task():
            response = self._get_response(url, headers=self.headers)
            return callback(response)

        return task

    def run(self):
        while True:
            try:
                task = self.tasks.pop(0)
                task()
            except IndexError:
                break

    def task_creator(self, urls: set, callback):
        urls_set = urls - self.done_url
        for url in urls_set:
            self.tasks.append(self.get_task(url, callback))
            self.done_url.add(url)

    def parse_feed(self, response: requests.Response):
        soup = bs4.BeautifulSoup(response.text, "lxml")
        ul_pagination = soup.find("ul", attrs={"class": "gb__pagination"})
        self.task_creator(
            {
                urljoin(response.url, a_tag.attrs["href"])
                for a_tag in ul_pagination.find_all("a")
                if a_tag.attrs.get("href")
            },
            self.parse_feed,
        )
        post_wrapper = soup.find("div", attrs={"class": "post-items-wrapper"})
        self.task_creator(
            {
                urljoin(response.url, a_tag.attrs["href"])
                for a_tag in post_wrapper.find_all("a", attrs={"class": "post-item__title"})
                if a_tag.attrs.get("href")
            },
            self.parse_post,
        )

    def parse_post(self, response: requests.Response):
        soup = bs4.BeautifulSoup(response.text, "lxml")
        author_name_tag = soup.find("div", itemprop="author")
        data = {
            "url": response.url,
            "title": soup.find("h1", attrs={"class": "blogpost-title"}).text,
            "author": {
                "url": urljoin(response.url, author_name_tag.parent.attrs.get("href")),
                "name": author_name_tag.text,
            },
        }
        self._save(data)

    def _save(self, data):
        collection = self.db["gb_parse_24_05"]["gb_parse"]
        collection.insert_one(data)


class GbBlogParseWithComments(GbBlogParse):

    headers_for_comments = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) "
                      "Gecko/20100101 Firefox/88.0",
        'range': None
    }

    __parse_time = 0

    def __init__(self, start_url, comments_api_url, db, delay=1.0):
        self.comments_api_url = comments_api_url
        GbBlogParse.__init__(self, start_url, db, delay=1.0)

    def _get_response(self, url, headers):
        while True:
            next_time = self.__parse_time + self.delay
            if next_time > time.time():
                time.sleep(next_time - time.time())
            response = requests.get(url, headers=headers)
            print(f"RESPONSE: {response.url}")
            self.__parse_time = time.time()
            if response.status_code == 200:
                return response

    def parse_post(self, response: requests.Response):
        soup = bs4.BeautifulSoup(response.text, "lxml")
        author_name_tag = soup.find("div", itemprop="author")
        comments_cnt = soup.find(name='comments')['total-comments-count']
        commentable_id = soup.find(name='comments')['commentable-id']
        data = {
            "url": response.url,
            "title": soup.find("h1", attrs={"class": "blogpost-title"}).text,
            'first_img_url': soup.find(name='div', attrs={'class': 'hidden', 'itemprop': 'image'}).text,
            'time': datetime.strptime(soup.find(name='time', attrs={'itemprop': 'datePublished'})['datetime'],
                                      '%Y-%m-%dT%H:%M:%S%z'),
            "author": {
                "url": urljoin(response.url, author_name_tag.parent.attrs.get("href")),
                "name": author_name_tag.text,
            },
            'comments': None if comments_cnt == '0' else self.parse_post_comments(commentable_id, comments_cnt)
        }
        self._save(data)

    def parse_post_comments(self, commentable_id, comments_cnt):

        def get_comments(comments):
            data = {}
            for comment in comments:
                data[f'author_{comment["comment"]["id"]}'] = comment['comment']['user']['full_name']
                data[f'text_{comment["comment"]["id"]}'] = comment['comment']['body']
                if 'children' in comment['comment'].keys():
                    data.update(get_comments(comment['comment']['children']))
            return data

        self.headers_for_comments['range'] = f'0-{comments_cnt}'
        response = self._get_response(f'{self.comments_api_url + commentable_id}',
                                      headers=self.headers_for_comments)
        comments = response.json()
        return get_comments(comments)


if __name__ == "__main__":
    db_client = pymongo.MongoClient("mongodb://localhost:27017")
    url = 'https://gb.ru/posts'
    comments_api_url = 'https://gb.ru/api/v2/comments?commentable_type=Post&order=desc&commentable_id='
    parser = GbBlogParseWithComments(url, comments_api_url, db_client, 0.5)
    parser.run()
