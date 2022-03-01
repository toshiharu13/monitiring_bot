import requests


def get_page(url):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
        }
    response = session.get(url, headers=headers)
    response.raise_for_status()
    return response


def main():
    monitoring_site_page = 'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/'
    site_page = get_page(monitoring_site_page)
    print(site_page.content.decode("utf-8"))


if __name__ == '__main__':
    main()


