import random
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

host_name = "localhost"
host_port = 8000


class Banner:
    def __init__(self, url, shows, categories):
        self.url = url
        self.shows = int(shows)
        self.categories = categories

    def __str__(self):
        return f'{self.url}: {self.shows}'

    def show(self):
        self.shows = self.shows - 1
        return self.shows


class BannerStore:
    def __init__(self):
        self.store = {}
        self.read_config()
        self.last_banner = None

    def __len__(self):
        return len(self.store)

    def read_config(self):
        with open('config.csv') as config:
            for line in config:
                data = line.strip().split(';')
                url = data[0]
                shows = data[1]
                categories = data[2:]
                self.put_banner(url, shows, categories)

    def put_banner(self, url, shows, categories):
        banner = Banner(url, shows, categories)
        for category in categories:
            if category not in self.store:
                self.store[category] = []
            self.store[category].append(banner)

    def remove_banner(self, banner):
        for category in banner.categories:
            self.store[category].remove(banner)

    def remove_empty_categories(self, categories):
        for category in categories:
            if self.is_category_empty(category):
                del self.store[category]

    def is_category_empty(self, category):
        return len(self.store[category]) == 0

    def get_banner_by_category(self, category):
        banner = random.choice(self.store[category])
        if banner.show() < 1:
            self.remove_banner(banner)
            self.remove_empty_categories(banner.categories)
        return banner

    def get_banner(self, categories=[], unique=True):
        categories = [c for c in categories if c in self.store]

        if not categories:
            categories = list(self.store.keys())

        if not categories:
            return

        category = random.choice(categories)
        banner = self.get_banner_by_category(category)

        if unique and banner is self.last_banner:
            self.get_banner_by_category(category)

        return banner


class BannerServer(BaseHTTPRequestHandler):
    def do_GET(self):
        qs = parse_qs(urlparse(self.path).query)
        if 'category[]' in qs:
            categories = qs['category[]']
            banner = bs.get_banner(categories)
            print(banner)
            if banner:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(f'<img src={banner.url} />', 'utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()


def run_server():
    banner_server = HTTPServer((host_name, host_port), BannerServer)
    print(time.asctime(), "Server Starts - %s:%s" % (host_name, host_port))

    try:
        banner_server.serve_forever()
    except KeyboardInterrupt:
        pass

    banner_server.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (host_name, host_port))


if __name__ == '__main__':
    bs = BannerStore()
    run_server()
