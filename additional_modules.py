import os
from urllib.parse import urljoin, urlsplit, unquote

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        raise requests.exceptions.HTTPError


def get_title_and_author(soup):
    title, author = soup.select_one('h1').text.split('::')
    book_name = sanitize_filename(title.strip())
    book_author = sanitize_filename(author.strip())
    return book_name, book_author


def parsing_picture_name_and_url(response, soup):
    picture_path = soup.select_one('.bookimage').find('img')['src']
    picture_url = urljoin(response.url, picture_path)
    picture_unq = unquote(picture_url)
    *_, picture_name = urlsplit(picture_unq).path.split('/')
    return picture_name, picture_unq


def download_image(picture_url, picture_name, dest_folder):
    img_response = requests.get(picture_url, allow_redirects=True)
    img_response.raise_for_status()
    check_for_redirect(img_response)

    folder = os.path.join(dest_folder, 'images') if dest_folder else 'images'
    if not os.path.exists(folder):
        os.makedirs(folder)

    img_path = os.path.join(folder, picture_name)
    with open(img_path, 'wb') as img_file:
        img_file.write(img_response.content)

    return img_path


def get_comments(soup):
    comments = ''
    pars_comments = soup.select('div.text')
    for comment in pars_comments:
        comment_row = comment.findNext('span', class_='black').text
        comments += f'\n{comment_row}'
    if not comments:
        comments = 'Нет комментариев'
    return comments


def get_genres(soup):
    genres = soup.select_one('span.d_book a')
    genres_text = ','.join([genre.text for genre in genres])
    return genres_text


def parse_book(response):
    soup = BeautifulSoup(response.text, 'lxml')

    title, author = get_title_and_author(soup)
    try:
        genres = get_genres(soup)
    except AttributeError:
        genres = 'Нет комментариев'

    try:
        comments = get_comments(soup)
    except AttributeError:
        comments = "Нет жанра"

    picture_name, picture_url = parsing_picture_name_and_url(response, soup)

    return {
        'title': title,
        'author': author,
        'genres': genres,
        'comments': comments,
        'picture_name': picture_name,
        'picture_url': picture_url
    }
