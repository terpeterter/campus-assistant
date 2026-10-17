"""Модуль поиска релевантных документов (Retrieval).

Ответственные разработчики: Пара 3 (Индексация и Поиск)
Задача:
1. Построить поисковый индекс BM25 по всем чанкам документов.
2. Принимать текстовый запрос от студента.
3. Возвращать топ-K самых релевантных фрагментов (SearchResult).
"""

from typing import List
from rank_bm25 import BM25Okapi
from core import Chunk, SearchResult


class BM25Retriever:
    def __init__(self, chunks: List[Chunk]):
        self.chunks = chunks
        # Простая токенизация (разбиение по пробелам и нижний регистр)
        self.tokenized_corpus = [self._tokenize(chunk.text) for chunk in chunks]
        if self.tokenized_corpus:
            self.bm25 = BM25Okapi(self.tokenized_corpus)
        else:
            self.bm25 = None

    def _tokenize(self, text: str) -> List[str]:
        """Очистка и разбивка текста на слова."""
        import re
        words = re.findall(r"\w+", text.lower())
        return words

    def search(self, query: str, top_k: int = 3) -> List[SearchResult]:
        """Поиск топ-K фрагментов по запросу."""
        if not self.bm25 or not self.chunks:
            return []

        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)

        # Сортируем по убыванию очков
        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

        results = []
        for idx in ranked_indices[:top_k]:
            score = scores[idx]
            if score > 0:  # Берем только если есть совпадения
                results.append(SearchResult(chunk=self.chunks[idx], score=float(score)))

        return results
