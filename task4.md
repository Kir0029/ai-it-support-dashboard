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