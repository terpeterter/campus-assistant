"""Общие структуры данных для всех модулей ассистента."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Chunk:
    """Один фрагмент документа с метаданными."""
    text: str                     # Сам текст фрагмента
    source: str                   # Имя исходного файла (например: "положение_о_стипендиях.pdf")
    page: Optional[int] = None    # Номер страницы (если это PDF)
    date: Optional[str] = None    # Дата документа (если известна)


@dataclass
class SearchResult:
    """Результат поиска по базе знаний."""
    chunk: Chunk                  # Найденный кусочек
    score: float                  # Оценка релевантности (чем выше, тем точнее совпадение)
