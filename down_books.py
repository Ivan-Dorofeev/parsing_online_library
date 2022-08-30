import argparse
import os

import requests

from bs4_tutorial import parse_book_page, download_images


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        print('Нет книги')
        raise requests.exceptions.HTTPError


def download_book(id_book, folder='books/'):
    url = f'https://tululu.org/b{id_book}'
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()

    check_for_redirect(response)

    if not os.path.exists(folder):
        os.makedirs(folder)

    download_images(response)

    parsing_book = parse_book_page(response)

    author_name = parsing_book['author']
    book_name = parsing_book['title']
    path_to_file = os.path.join(folder, f'{id_book}. {book_name}.txt')
    with open(path_to_file, 'wb') as ff:
        ff.write(response.content)

    print('Название: ', book_name)
    print('Автор: ', author_name, end='\n\n')
    return path_to_file


def main():
    parser = argparse.ArgumentParser(
        description='Скачиваем книги и выводим информацию по ним'
    )
    parser.add_argument('start_id', help='Начать с этого номера книги', default=1, type=int)
    parser.add_argument('end_id', help='Закончить этим номером книги', default=2, type=int)
    args = parser.parse_args()

    start_id = args.start_id
    end_id = args.end_id

    if end_id <= start_id:
        end_id = start_id + 1

    for id_book in range(start_id, end_id):
        try:
            download_book(id_book)
        except requests.exceptions.HTTPError:
            continue


if __name__ == '__main__':
    main()
