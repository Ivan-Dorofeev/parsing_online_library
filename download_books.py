import argparse
import os
import time

import requests

from parsing_modules import parse_book, download_image


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        raise requests.exceptions.HTTPError


def download_book(id_book, folder='books/'):
    url = f'https://tululu.org/b{id_book}'
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()

    check_for_redirect(response)

    if not os.path.exists(folder):
        os.makedirs(folder)

    download_image(response)

    parsed_book = parse_book(response)

    author_name = parsed_book['author']
    book_name = parsed_book['title']
    book_genre = parsed_book['genre']
    book_comments = parsed_book['comments']

    path_to_file = os.path.join(folder, f'{id_book}. {book_name}.txt')
    with open(path_to_file, 'wb') as ff:
        ff.write(response.content)
    return {'book_name': book_name, 'author_name': author_name, 'book_genre': book_genre,
            'book_comments': book_comments}


def main():
    parser = argparse.ArgumentParser(
        description='Скачиваем книги и выводим информацию по ним'
    )
    parser.add_argument('start_id', help='Начать с этого номера книги', nargs='?', default=1, type=int)
    parser.add_argument('end_id', help='Закончить этим номером книги', nargs='?', default=2, type=int)
    args = parser.parse_args()

    start_id = args.start_id
    end_id = args.end_id

    if end_id <= start_id:
        end_id = start_id + 1

    for id_book in range(start_id, end_id):
        try:
            downloaded_book = download_book(id_book)
            print('Название: ', downloaded_book['book_name'])
            print('Автор: ', downloaded_book['author_name'])
            print('Жанр: ', downloaded_book['book_genre'], end='\n\n')
            print('Комментарии: ', downloaded_book['book_comments'], end='\n\n')
        except requests.exceptions.HTTPError as exc:
            print("Ошибка: ", exc)
        except requests.exceptions.ConnectionError as exc:
            print("Ошибка: ", exc)
            print('Ожидаем соединение 5 минут')
            time.sleep(300)


if __name__ == '__main__':
    main()
