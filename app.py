import os
import json
import uuid
from datetime import datetime
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

try:
    from st_copy_to_clipboard import st_copy_to_clipboard
    COPY_ENABLED = True
except ImportError:
    COPY_ENABLED = False

load_dotenv()

HISTORY_FILE = "chat_history.json"

SYSTEM_PROMPT = (
    "Ты — внутренний IT-саппорт ассистент компании. "
    "Твоя задача: помогать сотрудникам с настройкой VPN, получением доступов, "
    "установкой ПО и решением технических проблем. "
    "Отвечай кратко, профессионально и по делу. "
    "Если вопрос не касается IT-инфраструктуры или работы компьютера, "
    "вежливо откажись отвечать, напомнив о своей специализации."
)

MODEL_NAME = os.getenv("MODEL_NAME", "qwen/qwen3.5-flash-02-23")


def get_default_data():
    return {
        "sessions": {},
        "order": [],
        "current_session_id": None
    }


def load_sessions():
    if not os.path.exists(HISTORY_FILE):
        return get_default_data()
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "sessions" in data:
            return data
        return get_default_data()
    except (json.JSONDecodeError, IOError):
        return get_default_data()


def save_sessions(data):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError:
        pass


def create_new_session(title="Новый чат"):
    session_id = str(uuid.uuid4())
    return session_id, {
        "title": title,
        "messages": []
    }


def get_session_title(messages):
    if not messages:
        return "Новый чат"
    first_user = next((m for m in messages if m["role"] == "user"), None)
    if first_user:
        title = first_user["content"][:30]
        return title + "..." if len(first_user["content"]) > 30 else title
    return "Новый чат"


def get_openai_client():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return None
    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )


def main():
    st.set_page_config(page_title="IT Support Assistant", page_icon="💻")

    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #0f172a 0%, #000000 100%);
    }
    [data-testid="stSidebar"] {
        background: #0f172a;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebarContent"] {
        background: #0f172a;
    }
    div[data-testid="stChatMessageContent"]:has(> div) {
        background: linear-gradient(135deg, #1e3a8a 0%, #312e81 100%);
        color: white;
        border-radius: 16px;
        padding: 12px 16px;
    }
    div[data-testid="chat-message-user"] [data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, #1e3a8a 0%, #312e81 100%);
    }
    div[data-testid="chat-message-assistant"] [data-testid="stChatMessageContent"] {
        background: #1e1e1e;
        border: 1px solid #333;
        border-radius: 16px;
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

    if "sessions_data" not in st.session_state:
        st.session_state.sessions_data = load_sessions()
        if not st.session_state.sessions_data["sessions"]:
            sid, session = create_new_session()
            st.session_state.sessions_data["sessions"][sid] = session
            st.session_state.sessions_data["order"].append(sid)
            st.session_state.sessions_data["current_session_id"] = sid
            save_sessions(st.session_state.sessions_data)

    data = st.session_state.sessions_data
    current_id = data.get("current_session_id")
    sessions = data["sessions"]
    order = data["order"]

    if current_id not in sessions:
        if order:
            current_id = order[-1]
        else:
            sid, session = create_new_session()
            sessions[sid] = session
            order.append(sid)
            current_id = sid
        data["current_session_id"] = current_id

    current_session = sessions.get(current_id, {"title": "Новый чат", "messages": []})
    messages = current_session["messages"]

    st.title("💻 IT Support Assistant")

    with st.sidebar:
        if st.button("➕ Новый чат", use_container_width=True):
            if messages:
                current_session["title"] = get_session_title(messages)
            sid, new_session = create_new_session()
            sessions[sid] = new_session
            order.insert(0, sid)
            data["current_session_id"] = sid
            save_sessions(data)
            st.rerun()

        st.markdown("---")
        st.text_input("🔍", placeholder="Поиск чатов...", key="search_query", label_visibility="collapsed")

        search = st.session_state.get("search_query", "").strip().lower()
        filtered_order = [
            sid for sid in order
            if search in sessions.get(sid, {}).get("title", "").lower()
        ] if search else order

        st.header("📜 Чаты")

        for sid in filtered_order:
            session = sessions.get(sid, {})
            title = session.get("title", "Новый чат")
            prefix = "👉 " if sid == current_id else "  "
            col1, col2 = st.columns([5, 1])
            with col1:
                if st.button(f"{prefix}💬 {title}", key=f"chat_{sid}", use_container_width=True):
                    if messages:
                        current_session["title"] = get_session_title(messages)
                    data["current_session_id"] = sid
                    save_sessions(data)
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"del_{sid}", help="Удалить чат"):
                    del sessions[sid]
                    order.remove(sid)
                    if sid == current_id:
                        if order:
                            data["current_session_id"] = order[0]
                        else:
                            new_sid, new_session = create_new_session()
                            sessions[new_sid] = new_session
                            order.append(new_sid)
                            data["current_session_id"] = new_sid
                    save_sessions(data)
                    st.rerun()

    for i, msg in enumerate(messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and COPY_ENABLED:
                st_copy_to_clipboard(msg["content"], key=f"copy_{i}")

    if prompt := st.chat_input("Задайте вопрос IT-специалисту..."):
        messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            client = get_openai_client()
            if not client:
                st.error("⚠️ API ключ не найден. Создайте файл .env с OPENROUTER_API_KEY")
            else:
                try:
                    api_messages = [
                        {"role": "system", "content": SYSTEM_PROMPT}
                    ] + [
                        {"role": m["role"], "content": m["content"]}
                        for m in messages
                    ]

                    placeholder = st.empty()
                    placeholder.markdown("⏳ **Думаю...**")

                    stream = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=api_messages,
                        stream=True
                    )

                    full_response = ""
                    for chunk in stream:
                        content = chunk.choices[0].delta.content or ""
                        full_response += content
                        placeholder.markdown(full_response + "▌")
                    placeholder.markdown(full_response)

                    messages.append({"role": "assistant", "content": full_response})
                    current_session["title"] = get_session_title(messages)
                    save_sessions(data)
                    st.rerun()

                except Exception:
                    st.error("⚠️ Ошибка связи с сервером AI. Пожалуйста, проверьте подключение или обратитесь к администратору.")


if __name__ == "__main__":
    main()
