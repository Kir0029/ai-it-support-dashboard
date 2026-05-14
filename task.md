Act as an expert Python developer. Your task is to build a web service — a mini-dashboard for an AI assistant — using Python and Streamlit. You must write clean, production-ready code with comments.

PROJECT OVERVIEW:
- Tech Stack: Python, Streamlit, openai (Python client), python-dotenv.
- Specialization: Internal IT-Support Assistant.
- API: OpenRouter (using the standard OpenAI library with custom base_url).

KEY FEATURES & REQUIREMENTS:
1. UI/UX:
- Use a Dark Theme for the Streamlit app.
- Layout: A sidebar on the left showing "Recent Chats" (history), and a main central area for the chat interface.
- Use `st.chat_message` and `st.chat_input` for the interface.

2. System Prompt & Persona:
- The AI must have a strict System Prompt: "Ты — внутренний IT-саппорт ассистент компании. Твоя задача: помогать сотрудникам с настройкой VPN, получением доступов, установкой ПО и решением технических проблем. Отвечай кратко, профессионально и по делу. Если вопрос не касается IT-инфраструктуры или работы компьютера, вежливо откажись отвечать, напомнив о своей специализации."
- This system prompt must be injected into the messages array sent to the API.

3. Streaming:
- The response from the LLM MUST be streamed to the UI chunk by chunk. Use `st.write_stream` or an equivalent Streamlit streaming generator.

4. Error Handling (Crucial):
- Wrap the API call in a try/except block. 
- If the API fails (e.g., no internet, invalid API key, OpenRouter downtime), DO NOT crash the app. Instead, catch the exception and display a user-friendly error message using `st.error` (e.g., "⚠️ Ошибка связи с сервером AI. Пожалуйста, проверьте подключение или обратитесь к администратору.").

5. History Persistence (Local Storage equivalent):
- To persist recent requests without a database, save the chat history to a local file named `chat_history.json`.
- When the app loads, read from this file so previous messages are displayed. Save new messages to this file automatically.

6. API Configuration (OpenRouter):
- Use the `openai` Python library.
- Set `base_url="https://openrouter.ai/api/v1"`.
- Use a placeholder model name (e.g., "openai/gpt-4o-mini" or "anthropic/claude-3-haiku") which the user can easily change.
- Load the API key from a `.env` file (OPENROUTER_API_KEY).

STEPS FOR YOU TO EXECUTE:
1. Create a `requirements.txt` file.
2. Create a `.env.example` file.
3. Create the main `app.py` file containing all the logic, UI, and state management.
4. If necessary, create a `.streamlit/config.toml` to enforce the dark theme.