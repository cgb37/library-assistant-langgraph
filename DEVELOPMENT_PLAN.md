# DEVELOPMENT_PLAN.md

## Goal
Integrate the LangGraph-powered library assistant from [`main.py`](main.py) into the Quart web app, allowing users to submit prompts via the chat UI and receive responses in the browser.

---

## Phase 1: Minimal Integration

1. **Refactor `main.py` Logic**
   - Move the core assistant logic (graph creation and invocation) into functions/classes that can be imported and called from the Quart app.

2. **Quart Backend API**
   - Add a `/chat` POST endpoint to [`app.py`](app.py) that accepts a user prompt and returns the assistant's response as JSON.

3. **Frontend Integration**
   - Update [`static/chatui.js`](static/chatui.js) to submit chat messages to the `/chat` endpoint via AJAX/fetch.
   - Display the assistant's response in the chat window.

---

## Phase 2: Basic Robustness

4. **Error Handling**
   - Add basic error handling for invalid input and backend errors (both in backend and frontend).

5. **UI Feedback**
   - Show loading indicators while waiting for a response.

---

## Phase 3: (Optional, for future)
- Add user session support.
- Persist chat history.
- Add tests and linting.
- Add CRUD for projects.
  - Allow users to create projects with a name and description.
  - Display the list of projects in the right sidebar.
  - (Eventually) Associate chats with projects.

---

## Questions

1. Should the chat be single-turn (one question/response at a time) or multi-turn (maintain conversation history)?
2. Do you want to keep the CLI interface in [`main.py`](main.py) or move entirely to the web UI?
3. Any authentication or access restrictions needed for the chat interface?
4. Should we support both undergraduate and graduate routing in the UI, or just show the assistant's response?

---

Let me know your preferences or if you want to adjust the plan!