import requests


class Onion:

    @staticmethod
    def send(url):
        proxies = {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050'
        }
        r = requests.get(url, proxies=proxies)
        print(r.text)
