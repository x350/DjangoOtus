import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
from multiprocessing import Pool
import argparse


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except:
        return ''
    if response.ok:
        return response.text


def get_list_link(response):
    if response:
        soup = BeautifulSoup(response, 'lxml')
        links = soup.find_all('a')
        return links
    else:
        return []


def prepare_links(links, parent_url):
    set_href = set()
    for link in links:
        href = link.get('href')

        if href:
            link = urljoin(parent_url, href)
            if 'http' in link:
                set_href.add(link)
    return list(set_href)


def make_list_from_url(url):
    links = get_list_link(get_html(url))
    pure_links = prepare_links(links, url)
    return pure_links


def make_finali_list(links_list):
    # summ = 0
    union_set = set()
    for item in links_list:
        # summ += len(item)
        union_set = union_set.union(item)
    # print(summ)
    return list(union_set)


def write_txt(name, data):
    with open(name, 'a') as file:
        file.write(', '.join(data))


def main():
    parser = argparse.ArgumentParser(description='Search for links in an HTML page by a given URL.')
    parser.add_argument('url', help="Input site url.")
    parser.add_argument( '-s', '--save_to_file', nargs='?', help="Save to file .csv.")
    args = parser.parse_args()

    pure_links = make_list_from_url(args.url)
    with Pool(20) as p:
        list_list_links = p.map(make_list_from_url, pure_links)
    result = make_finali_list(list_list_links)

    if args.save_to_file:
        write_txt(args.save_to_file, result)
    else:
        print(result)
        print(f"Найдено {len(result)} ссылок.")


if __name__ == '__main__':
    main()
