import requests


class Onion:

    _proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }

    @staticmethod
    def get(url, params=None, **kwargs):
        kwargs.update({'proxies': Onion._proxies})
        return requests.get(url, params=params, **kwargs)

    @staticmethod
    def options(url, **kwargs):
        kwargs.update({'proxies': Onion._proxies})
        return requests.options(url, **kwargs)

    @staticmethod
    def head(url, **kwargs):
        kwargs.update({'proxies': Onion._proxies})
        return requests.head(url, **kwargs)

    @staticmethod
    def post(url, data=None, json=None, **kwargs):
        kwargs.update({'proxies': Onion._proxies})
        return requests.post(url, data=data, json=json, **kwargs)

    @staticmethod
    def put(url, data=None, **kwargs):
        kwargs.update({'proxies': Onion._proxies})
        return requests.put(url, data=data, **kwargs)

    @staticmethod
    def patch(url, data=None, **kwargs):
        kwargs.update({'proxies': Onion._proxies})
        return requests.patch(url, data=data, **kwargs)

    @staticmethod
    def delete(url, **kwargs):
        kwargs.update({'proxies': Onion._proxies})
        return requests.delete(url, **kwargs)
