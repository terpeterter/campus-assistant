"""Модуль загрузки и нарезки документов.

Ответственный разработчик: Разработчик 2 (Загрузка данных)
Задача:
1. Прочитать файлы из папки data/documents/ (PDF, MD, TXT).
2. Разбить длинные тексты на небольшие смысловые части (чанки по 300-500 слов).
3. Вернуть список объектов Chunk.
"""

import os
import sys
from typing import List
import pymupdf  # PyMuPDF

# Добавляем корень проекта в путь поиска модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core import Chunk


def load_text_file(file_path: str) -> List[Chunk]:
    """Чтение .txt и .md файлов."""
    filename = os.path.basename(file_path)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # Простая разбивка по абзацам (заготовка)
    paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 30]
    return [Chunk(text=p, source=filename) for p in paragraphs]


def load_pdf_file(file_path: str) -> List[Chunk]:
    """Чтение .pdf файлов постранично."""
    filename = os.path.basename(file_path)
    chunks = []
    doc = pymupdf.open(file_path)

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text().strip()
        if text:
            chunks.append(Chunk(text=text, source=filename, page=page_num + 1))

    doc.close()
    return chunks


def load_all_documents(folder_path: str = "data/documents") -> List[Chunk]:
    """Основная функция: загружает все поддерживаемые файлы из папки."""
    all_chunks = []
    if not os.path.exists(folder_path):
        return all_chunks

    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if not os.path.isfile(full_path):
            continue

        if filename.endswith((".txt", ".md")):
            all_chunks.extend(load_text_file(full_path))
        elif filename.endswith(".pdf"):
            all_chunks.extend(load_pdf_file(full_path))

    return all_chunks


if __name__ == "__main__":
    # Быстрый тест модуля при запуске напрямую
    chunks = load_all_documents()
    print(f"Загружено фрагментов: {len(chunks)}")
    if chunks:
        print(f"Пример первого фрагмента из [{chunks[0].source}]:")
        print(chunks[0].text[:200] + "...")
