Act as an expert UI/UX developer. I want to dramatically improve the visual design of my current Streamlit app using custom CSS injected via `st.markdown("<style>...</style>", unsafe_allow_html=True)`. 

Please add a custom CSS block at the top of my app to implement a "Modern Dark Gradient" theme. 

Requirements for the CSS:
1. Main Background (`[data-testid="stAppViewContainer"]`): Apply a smooth, dark linear gradient (e.g., from deep dark blue #0f172a to rich black #000000).
2. Sidebar (`[data-testid="stSidebar"]`): Make it a solid dark color with a subtle right border to separate it from the main content.
3. User Chat Bubbles: Give user messages a vibrant blue/purple gradient background (like `#1e3a8a` to `#312e81`), rounded corners, and white text. Align them nicely.
4. Assistant Chat Bubbles: Give assistant messages a sleek dark-gray background (e.g., `#1e1e1e`) with a subtle border or shadow.
5. Hide the default Streamlit top header line if possible to make it look like a standalone native app.