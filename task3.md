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