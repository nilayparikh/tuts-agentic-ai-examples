# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `1b37e3ba-dd81-4b8a-9c2e-f603573ac76e`  
> - **Started:** 12/03/2026, 20:11:17  
> - **Duration:** 33s  
> - **Exported:** 12/03/2026, 20:11:50  

---

<sub>⏱️ 5s</sub>

### 👤 User

Add a new API endpoint for loan notification preferences.

---

<sub>⏱️ 10s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\01-why-context-engineering\without-context.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\01-why-context-engineering\without-context

```
app
README.md
```


---

<sub>⏱️ 13s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\01-why-context-engineering\without-context\app.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\01-why-context-engineering\without-context\app

```
api
```


---

<sub>⏱️ 13s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\01-why-context-engineering\without-context\README.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\01-why-context-engineering\without-context\README.md

<details>
<summary>38 lines</summary>

```
1. # Without Context — Baseline
2. 
3. This folder simulates a **bare repository** with no AI guidance files. There are
4. no `.github/` instructions, no `docs/` architecture references, and no framework
5. hints.
6. 
7. ## What Happens Here
8. 
9. When you ask Copilot to "add a loan notification preferences endpoint" in this
10. folder, the assistant has **no way to know**:
11. 
12. - That the project uses **FastAPI** (not Flask, not Django)
13. - That routes use **APIRouter** with versioned prefixes
14. - That data access uses **async SQLAlchemy** with dependency injection
15. - That response models are **Pydantic** classes with explicit field definitions
16. 
17. The result is typically a Flask app with hardcoded data — a reasonable guess for
18. a generic Python web project, but wrong for this one.
19. 
20. ## File
21. 
22. - `app/api/preferences.py` — The AI-generated endpoint (Flask, no type hints,
23.   hardcoded response, no async, no DI)
24. 
25. ## What to Observe
26. 
27. Open `app/api/preferences.py` and note:
28. 
29. 1. **Wrong framework**: Flask instead of FastAPI
30. 2. **No type safety**: No Pydantic models or type annotations
31. 3. **No async**: Synchronous handler
32. 4. **No dependency injection**: Hardcoded response, no database session
33. 5. **No versioning**: Plain `/preferences` route, no prefix convention
34. 6. **No error handling**: No structured error responses
35. 
36. These are not mistakes in the AI — they are the natural result of **zero project
37. context**. The AI defaulted to the most common Python web framework.
38.
```

</details>


---

<sub>⏱️ 16s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\01-why-context-engineering\without-context\app\api.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\01-why-context-engineering\without-context\app\api

```
preferences.py
```


---

<sub>⏱️ 18s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\01-why-context-engineering\without-context\app\api\preferences.py.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\01-why-context-engineering\without-context\app\api\preferences.py

<details>
<summary>40 lines</summary>

```
1. """Generic example output for a repo with no project context.
2. 
3. This file intentionally represents the kind of framework-agnostic or incorrect
4. output a coding assistant may produce when the repository does not describe the
5. actual stack, conventions, or architecture.
6. """
7. 
8. from flask import Flask, jsonify
9. 
10. 
11. app = Flask(__name__)
12. 
13. 
14. @app.route("/preferences", methods=["GET"])
15. def get_preferences() -> object:
16.     """Return a hard-coded preferences payload."""
17.     return jsonify({"notifications": {"email": True, "sms": False}})
18. 
19. 
20. @app.route("/preferences/loans", methods=["GET"])
21. def get_loan_notification_preferences() -> object:
22.     """Return hard-coded loan notification preferences."""
23.     return jsonify({
24.         "loan_notifications": {
25.             "due_date_reminder": True,
26.             "payment_confirmation": True,
27.             "overdue_alert": True,
28.             "rate_change": False,
29.             "channel": "email"
30.         }
31.     })
32. 
33. 
34. @app.route("/preferences/loans", methods=["POST"])
35. def update_loan_notification_preferences() -> object:
36.     """Update loan notification preferences (stub — no persistence)."""
37.     from flask import request
38.     data = request.get_json() or {}
39.     return jsonify({"status": "updated", "preferences": data})
40.
```

</details>


---

<sub>⏱️ 33s</sub>

### 💬 Copilot

The endpoint already exists in `app/api/preferences.py`. This file is the pre-populated "without context" example for the tutorial — it demonstrates exactly what gets generated without project context:

- **Flask** instead of FastAPI
- **Hardcoded** response data, no DB access
- **No async**, no Pydantic models, no dependency injection
- **No versioned prefix** (plain `/preferences/loans`)

The file contains:
- `GET /preferences/loans` — returns hardcoded loan notification flags
- `POST /preferences/loans` — stub update with no persistence

This is intentional per the `README.md`: it illustrates how a coding assistant defaults to the most common Python web framework (Flask) when given zero project context.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
