import requests


def main():
    proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
    }
    r = requests.get('https://httpbin.org/get', proxies=proxies)
    print(r.text)


if __name__ == '__main__':
    main()
