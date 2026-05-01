# Spec: Login and Logout

## Overview

This feature implements user authentication for the Spendly expense tracker. It enables users to log in with their registered email and password, and log out to end their session. Login is the gateway to all protected routes (profile, expenses), while logout securely terminates the user session. This step builds on the registration system from Step 2.

## Depends on

- Step 1 (Database Setup) — users table and helper functions
- Step 2 (Registration) — user creation and password hashing

## Routes

| Route | Method | Description | Access |
|-------|--------|-------------|--------|
| `/login` | GET, POST | Display login form and process authentication | Public |
| `/logout` | GET | Clear session and redirect to login | Logged-in |

## Database changes

No database changes — uses existing `users` table from Step 1.

## Templates

- **Modify:** `templates/login.html` — add form with email/password fields, error display, and submit button
- **Create:** None (login.html exists but needs implementation)

## Files to change

- `app.py` — implement POST handler for `/login` route with credential validation
- `database/db.py` — add `verify_user_password(email, password)` helper
- `templates/login.html` — replace placeholder with working login form
- `templates/base.html` — add session-aware navigation (show logout when logged in)

## Files to create

None.

## New dependencies

No new dependencies — uses existing `werkzeug.security` for password verification.

## Rules for implementation

- Use Flask sessions for authentication state (`session['user_id']`)
- Password verification must use `werkzeug.security.check_password_hash()`
- All queries parameterized with `?` placeholders — never f-strings in SQL
- Session-based auth check: redirect to `/login` if `user_id` not in session
- Use CSS variables from `style.css` — never hardcode hex values
- All templates extend `base.html`
- After successful login: redirect to `/profile`
- After logout: redirect to `/login`
- Display flash messages for login/logout feedback

## Definition of done

- [ ] GET `/login` renders login form with email and password fields
- [ ] POST `/login` validates credentials against database
- [ ] Invalid credentials show error message on login page
- [ ] Valid credentials set session and redirect to `/profile`
- [ ] GET `/logout` clears session and redirects to `/login`
- [ ] Protected routes (e.g., `/profile`) redirect to `/login` when not authenticated
- [ ] Navigation in `base.html` shows "Logout" link when logged in
- [ ] App runs without errors on port 5001
