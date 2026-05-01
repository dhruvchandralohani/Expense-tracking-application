# Spec: Registration

## Overview

Implement the backend logic for user registration. The registration page (`/register`) already exists as a template with a POST form. This step adds the server-side handling to accept form submissions, validate input, hash passwords, and create new user accounts in the database.

## Depends on

- Step 01 (Database Setup) — the `users` table and `get_db()` function must exist

## Routes

- `POST /register` — Handle registration form submission — public

## Database changes

No database changes — the `users` table from Step 01 is sufficient.

## Templates

- **Modify:** `templates/register.html`
  - Add `method="POST"` to the form (already present)
  - Add `value="{{ request.form.name }}"` to preserve input on error
  - Add success flash message handling if flash is used

## Files to change

- `app.py` — Add POST handler for `/register` route
- `database/db.py` — Add `create_user()` function
- `templates/register.html` — Preserve form values on validation error

## Files to create

- None

## New dependencies

No new dependencies.

## Rules for implementation

- No SQLAlchemy or ORMs — raw SQLite only
- Parameterized queries only (`?` placeholders) — never f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate: email format, password length (min 8 chars), required fields
- Return 400 with error message for validation failures
- Use `abort(400)` for validation errors, not bare string returns
- Check for duplicate email before inserting

## Definition of done

- [ ] POST `/register` accepts form data (name, email, password)
- [ ] Input validation: rejects empty fields, invalid email, password < 8 chars
- [ ] Duplicate email check: shows error if email already registered
- [ ] Password is hashed before storing in database
- [ ] New user is inserted into `users` table
- [ ] On success: redirects to login page
- [ ] On error: re-renders registration form with error message and preserved input
- [ ] Form fields preserve values on validation error (except password)
- [ ] No raw passwords stored in database
