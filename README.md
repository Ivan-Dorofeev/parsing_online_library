## Парсер книг с сайта tululu.org

Скрипт скачивает по указанным id книги из онлайн библиотеки: https://tululu.org .

### Описание
Все книги скачиваются в папку ```"/books"``` .

Также скачивают отдельно картинки их обложек, если они есть в папку ```"/images"``` .

Также все данные по скаченным книгам записываются в файл ```downloaded_books.json```

В консоль выводится информация о книгах:
- название книги
- автор книги
- жанр книги
- комментарии посетителей ( если они есть )

### Как установить

- скачать репозиторий
- установите необходимы библиотеки командой:

    ```pip install -r requirements.txt```

### Запуск

Чтобы запустить скрипт, выполните команду:

    ```python download_books.py```

Фильтры для скачивания:

```--start_page``` - Начать с этой страницы

```--end_page``` - Закончить на этой странице

```--dest_folder``` - Путь к каталогу с результатами парсинга

```--skip_imgs``` - Не скачивать картинки

```--skip_txt``` - Не скачивать книги

```--json_path``` - Указать свой путь к *.json файлу с результатами

После запуска вы получите следующее:

![image](https://user-images.githubusercontent.com/58893102/187357187-10d250db-1eea-4ad7-8b00-7b9a330382eb.png)

