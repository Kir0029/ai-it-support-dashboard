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

---

Act as an expert UI/UX developer. I want to dramatically improve the visual design of my current Streamlit app using custom CSS injected via `st.markdown("<style>...</style>", unsafe_allow_html=True)`. 

Please add a custom CSS block at the top of my app to implement a "Modern Dark Gradient" theme. 

Requirements for the CSS:
1. Main Background (`[data-testid="stAppViewContainer"]`): Apply a smooth, dark linear gradient (e.g., from deep dark blue #0f172a to rich black #000000).
2. Sidebar (`[data-testid="stSidebar"]`): Make it a solid dark color with a subtle right border to separate it from the main content.
3. User Chat Bubbles: Give user messages a vibrant blue/purple gradient background (like `#1e3a8a` to `#312e81`), rounded corners, and white text. Align them nicely.
4. Assistant Chat Bubbles: Give assistant messages a sleek dark-gray background (e.g., `#1e1e1e`) with a subtle border or shadow.
5. Hide the default Streamlit top header line if possible to make it look like a standalone native app.

---

Act as an expert Streamlit developer. My app looks great, but I need to add two critical features to improve the UX. Please update the code in `app.py`:

1. "New Chat" Button:
Add a button at the very top of the sidebar labeled "➕ Новый чат" (New Chat). 
When this button is clicked, it MUST:
- Clear the `st.session_state.messages` list.
- Overwrite the `chat_history.json` file with an empty list `[]`.
- Immediately call `st.rerun()` so the chat interface visually clears instantly.
(You can remove the old "Очистить историю" button if it exists, replacing it with this new logic).

2. "Copy Response" Button:
Underneath each of the Assistant's messages in the chat history, add a "📋 Скопировать" (Copy) button.
CRITICAL: Do NOT use backend libraries like `pyperclip` because they won't work in the user's browser if deployed. 
Instead, use a frontend-friendly method. You can either use a lightweight HTML/JS snippet via `st.components.v1.html` to copy the text to the clipboard, OR use a known Streamlit library like `streamlit-clipboard` or `st_copy_to_clipboard` (if you choose a library, remember to update `requirements.txt`).
Make sure the copy button looks neat and doesn't break the UI.

---

Act as an expert Streamlit developer. There are two major issues in the current code that need to be fixed immediately.

ISSUE 1: The "Copy" button is broken.
It renders as raw HTML text (e.g., `<button onclick="...">`) inside the chat message, especially after refreshing the page. Streamlit is escaping the HTML.
FIX 1: Do NOT append raw HTML strings to the assistant's message text! 
To fix this, you must use the `st_copy_to_clipboard` library (add `st-copy-to-clipboard` to requirements.txt). 
Place the `st_copy_to_clipboard(text=assistant_response, key=...)` right under the `st.chat_message("assistant")` block. 
If you cannot implement the copy button cleanly without breaking the chat UI or showing raw HTML, completely REMOVE the copy button feature. A clean UI is more important.

ISSUE 2: "New Chat" logic deletes all history.
Currently, clicking "New Chat" overwrites `chat_history.json` with `[]`. The user wants to KEEP past chats (like ChatGPT).
FIX 2: Redesign the history logic to support multiple sessions:
- Update `chat_history.json` to store a DICTIONARY of sessions, where the key is the session name (e.g., "Chat YYYY-MM-DD HH:MM") and the value is the list of messages.
- State Management: Track `st.session_state.current_session_id`. If it doesn't exist, create a default one.
- Sidebar UI: Under the "➕ Новый чат" button, iterate over the keys in `chat_history.json` and display them as `st.sidebar.button`. If a user clicks a past session button, change `st.session_state.current_session_id` to that key and load its messages.
- "New Chat" button behavior: Generate a new session key, clear `st.session_state.messages`, set the new key as active, and call `st.rerun()`.
- Saving: Whenever a new message is generated, append it to `st.session_state.messages` AND save it to the current active session key in the `chat_history.json` dictionary.

Please rewrite the necessary parts of `app.py` to implement this multi-session history and fix the HTML bug.