# Spec: Login and Logout

## Overview
This step wires up the existing `/login` page (currently a static GET-only template) into a working
sign-in flow, and implements the currently-stubbed `/logout` route. Submitting the login form looks up
the user by email, verifies the password against its stored hash, starts a logged-in session, and
redirects into the app; hitting `/logout` clears that session. This completes the authentication loop
started in Step 2 (Registration) — together, registration, login, and logout are the session mechanism
every later step (profile, expenses) depends on.

## Depends on
- Step 1 (Database setup) — `users` table and `get_db()`/`init_db()`/`seed_db()` must exist and work.
- Step 2 (Registration) — `create_user()`, `app.secret_key`, and the `session["user_id"]` convention
  established during registration must already be in place.

## Routes
- `GET /login` — render the sign-in form (already exists, unchanged) — public
- `POST /login` — validate credentials, start session, redirect to `/` — public
- `GET /logout` — clear the session and redirect to `/` — logged-in (no-op redirect if already logged out)

`/login` becomes a combined `GET`/`POST` route (`methods=["GET", "POST"]`) rather than a new path.
`/logout` replaces its current placeholder body (`"Logout — coming in Step 3"`).

## Database changes
No new tables or columns. The `users` table (`id`, `name`, `email`, `password_hash`, `created_at`)
already supports login as defined in `database/db.py`. Add one helper function to `database/db.py`:
- `get_user_by_email(email)` — runs a parameterized `SELECT` against `users` for the given (lowercased,
  stripped) email and returns the row (or `None` if no match), so `app.py` can verify the password with
  `werkzeug.security.check_password_hash` without embedding SQL in the route handler.

## Templates
- **Create:** none
- **Modify:**
  - `templates/login.html` — no structural changes; it already posts to `/login` and already renders
    `{{ error }}` when present, so the existing markup is reused as-is by the new route logic.
  - `templates/base.html` — the navbar currently hardcodes "Sign in" / "Get started" links regardless of
    session state. Use the `session` object (available by default in Jinja) to conditionally render
    "Logout" when `session.user_id` is set, otherwise the existing "Sign in" / "Get started" links. This
    is the only way to reach `/logout` from the UI, so it's required for this step to be testable
    end-to-end.

## Files to change
- `app.py` — change `/login` to accept `GET`/`POST`, add credential validation (look up the user via
  `database.db.get_user_by_email`, verify the password with `check_password_hash`), start the session
  (`session["user_id"]`) on success, redirect to `/`. Replace the `/logout` placeholder with logic that
  calls `session.clear()` (or `session.pop("user_id", None)`) and redirects to `/`.
- `database/db.py` — add `get_user_by_email(email)`.
- `templates/base.html` — conditional nav links based on `session.user_id`.

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs.
- Parameterised queries only.
- Passwords hashed with `werkzeug.security` — verify with `check_password_hash`, never compare plaintext.
- Use CSS variables — never hardcode hex values.
- All templates extend `base.html`.
- Re-render `login.html` with a generic `error` message ("Invalid email or password.") on unknown email
  or wrong password — never reveal which of the two was wrong, and never expose a raw stack trace.
- Validate on the server even though the form has `required`/`type=email` attributes client-side.

## Definition of done
- [ ] Logging in with the seeded demo account (`demo@spendly.com` / `demo123`) sets `session["user_id"]`
      and redirects away from `/login`.
- [ ] Logging in with a correct email but wrong password re-renders `login.html` with a generic error and
      does not start a session.
- [ ] Logging in with an email that doesn't exist re-renders `login.html` with the same generic error
      (no indication the account doesn't exist).
- [ ] Submitting with a missing email or password re-renders the form with an error instead of crashing.
- [ ] Visiting `/logout` while logged in clears the session and redirects to `/`; the navbar reverts to
      showing "Sign in" / "Get started".
- [ ] While logged in, the navbar shows a "Logout" link (and no "Sign in" link); clicking it logs out.
- [ ] `GET /login` still renders the plain form as before.
- [ ] App starts and runs without errors (`./venv/Scripts/python.exe app.py`).
