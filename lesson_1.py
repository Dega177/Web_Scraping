from pathlib import Path
import json
import time
import requests


class Parse5ka:
    headers = {"User-Agent": "Philipp Kirkorov"}

    def __init__(self, start_url: str, save_dir: Path):
        self.start_url = start_url
        self.save_dir = save_dir

    def _get_response(self, url: str) -> requests.Response:
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(0.2)

    def run(self):
        for product in self._parse(self.start_url):
            file_name = f"{product['id']}.json"
            file_path = self.save_dir.joinpath(file_name)
            self._save(product, file_path)

    def _parse(self, url):
        while url:
            response = self._get_response(url)
            data = response.json()
            url = data["next"]
            for product in data["results"]:
                yield product

    def _save(self, data: dict, file_path: Path):
        file_path.write_text(json.dumps(data, ensure_ascii=False))


def get_dir_path(dir_name: str) -> Path:
    dir_path = Path(__file__).parent.joinpath(dir_name)
    if not dir_path.exists():
        dir_path.mkdir()
    return dir_path


class CategoryParser(Parse5ka):

    def __init__(self, start_url: str, categories_url: str, save_dir: Path):
        self.categories_url = categories_url
        Parse5ka.__init__(self, start_url, save_dir)

    def run(self):
        for category_items in self._parse(self.start_url):
            file_name = f"{category_items['name']}.json"
            file_path = self.save_dir.joinpath(file_name)
            self._save(category_items, file_path)

    def _parse(self, url):
        for parent_group_code in self._get_parent_group_code(self.categories_url):
            response = self._get_response(f'{self.categories_url}+{parent_group_code}')
            child_categories = response.json()
            for category in child_categories:
                category_url = f'{url}+{category["group_code"]}'
                category_items = {'name': category["group_name"], 'code': category["group_code"], 'products': []}
                while category_url:
                    response = self._get_response(category_url)
                    items = response.json()
                    category_url = items['next']
                    if not items['results']: break
                    category_items['products'].append(items['results'])
                else:
                    yield category_items

    def _get_parent_group_code(self, categories_url):
        response = requests.get(categories_url, headers=self.headers)
        categories = response.json()
        for category in categories:
            yield category['parent_group_code']


if __name__ == "__main__":
    start_url = 'https://5ka.ru/api/v2/special_offers/?categories='
    categories_url = 'https://5ka.ru/api/v2/categories/'
    save_dir = get_dir_path("groups")
    parser = CategoryParser(start_url, categories_url, save_dir)
    parser.run()
