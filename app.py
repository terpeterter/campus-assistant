"""Веб-интерфейс ИИ-ассистента для цифрового кампуса Московского Политеха.

Ответственные разработчики: Пара 5 (Streamlit UI)
"""

import streamlit as st
from core.document_loader import load_all_documents
from core.retriever import BM25Retriever
from core.llm_client import LLMClient

# Настройка страницы
st.set_page_config(
    page_title="ИИ-ассистент кампуса | Московский Политех",
    page_icon="🎓",
    layout="centered"
)

# Кэшируем загрузку документов и индекс, чтобы не пересчитывать при каждом сообщении
@st.cache_resource
def init_system():
    chunks = load_all_documents("data/documents")
    retriever = BM25Retriever(chunks)
    llm = LLMClient()
    return chunks, retriever, llm

chunks, retriever, llm = init_system()

# Заголовок и описание
st.title("🎓 Цифровой кампус: ИИ-ассистент")
st.caption("Официальный консультант первокурсника Московского Политеха")

# Боковая панель с информацией о базе знаний
with st.sidebar:
    st.header("📚 База знаний")
    st.write(f"Загружено фрагментов: **{len(chunks)}**")
    if chunks:
        unique_sources = sorted(list(set(c.source for c in chunks)))
        st.write("Документы в базе:")
        for s in unique_sources:
            st.markdown(f"- `{s}`")
    
    st.divider()
    st.info("💡 Ассистент отвечает только по официальным документам вуза.")

# Хранилище истории диалога в сессии
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Привет! Я твой цифровой помощник. Задай любой вопрос про учёбу, стипендии, справки или жизнь в кампусе."}
    ]

# Отрисовка истории сообщений
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ввод нового вопроса
if prompt := st.chat_input("Например: как получить социальную стипендию?"):
    # Добавляем вопрос пользователя
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Поиск и генерация ответа
    with st.chat_message("assistant"):
        with st.spinner("Ищу информацию в документах университета..."):
            # 1. Ищем релевантные куски
            search_results = retriever.search(prompt, top_k=3)
            context_chunks = [res.chunk for res in search_results]

            # 2. Генерируем ответ
            answer = llm.generate_answer(prompt, context_chunks)
            st.markdown(answer)

            # 3. Показываем источники в выпадающем блоке
            if context_chunks:
                with st.expander("🔍 Посмотреть найденные источники"):
                    for i, res in enumerate(search_results, 1):
                        meta = f"**{res.chunk.source}**"
                        if res.chunk.page:
                            meta += f" (стр. {res.chunk.page})"
                        st.markdown(f"{i}. {meta} — *соответствие: {res.score:.2f}*")
                        st.caption(f"> {res.chunk.text[:200]}...")

    # Сохраняем ответ ассистента в историю
    st.session_state.messages.append({"role": "assistant", "content": answer})
