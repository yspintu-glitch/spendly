# Spec: Registration

## Overview
This step wires up the existing `/register` page (currently a static GET-only template) into a working
account-creation flow. Submitting the form validates input, checks for a duplicate email, hashes the
password with `werkzeug`, inserts a new row into `users`, starts a logged-in session, and redirects the
new user into the app. This is the first authentication feature built on top of the database layer from
Step 1, and every later step (login, logout, profile, expenses) depends on the session mechanism it
introduces.

## Depends on
- Step 1 (Database setup) — `users` table and `get_db()`/`init_db()`/`seed_db()` must exist and work.

## Routes
- `GET /register` — render the registration form (already exists, unchanged) — public
- `POST /register` — validate input, create the user, start session, redirect to `/` (or profile once it
  exists) — public

`/register` becomes a combined `GET`/`POST` route (`methods=["GET", "POST"]`) rather than a new path.

## Database changes
No database changes. The `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) already
supports registration as defined in `database/db.py`. Add one helper function to `database/db.py`:
- `create_user(name, email, password)` — hashes the password with `generate_password_hash` and inserts
  the row via a parameterized `INSERT`; lets a `sqlite3.IntegrityError` (duplicate email) propagate to the
  caller so `app.py` can turn it into a friendly form error.

## Templates
- **Create:** none
- **Modify:** `templates/register.html` — no structural changes; it already posts to `/register` and
  already renders `{{ error }}` when present, so the existing markup is reused as-is by the new route
  logic.

## Files to change
- `app.py` — set `app.secret_key` (read from env or a dev default), change `/register` to accept
  `GET`/`POST`, add form validation, call `database.db.create_user`, start the session
  (`session["user_id"]`), redirect on success.
- `database/db.py` — add `create_user(name, email, password)`.

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs.
- Parameterised queries only.
- Passwords hashed with `werkzeug.security.generate_password_hash`.
- Use CSS variables — never hardcode hex values.
- All templates extend `base.html`.
- Re-render `register.html` with an `error` message on invalid/duplicate input instead of raising an
  unhandled exception — never expose a raw stack trace to the user.
- Validate on the server even though the form has `required`/`type=email` attributes client-side.

## Definition of done
- [ ] Submitting the form with a new name/email/password creates a row in `users` with a hashed
      (non-plaintext) password.
- [ ] After successful registration, the user is redirected away from `/register` and `session["user_id"]`
      is set.
- [ ] Registering with an email that already exists re-renders `register.html` with an error message and
      does not create a duplicate row.
- [ ] Submitting with a missing name, email, or password re-renders the form with an error instead of
      crashing.
- [ ] `GET /register` still renders the plain form as before.
- [ ] App starts and runs without errors (`./venv/Scripts/python.exe app.py`).
