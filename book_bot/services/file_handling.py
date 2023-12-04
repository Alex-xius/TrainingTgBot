import os
import sys

BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


# Функция, возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    end_simbol = ['.', ',', '!', ':', ';', '?']
    end = start+page_size
    while text[end:][:1] in end_simbol:
        end -= 1
    text = text[start:end]
    text = text[: max(map(text.rfind, end_simbol))+1]
    return text, len(text)


# Функция, формирующая словарь книги
def prepare_book(path: str) -> None:
    with open(path, 'r', encoding="utf-8") as file:
        text = file.read()
    lenght = len(text)
    start = 0
    number_page = 0
    while start < lenght:
        page, l = _get_part_text(text, start, PAGE_SIZE)
        start += l
        number_page += 1
        book[number_page] = page.lstrip()


# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))
