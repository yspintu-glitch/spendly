# Spec: Profile Page Design

## Overview
This step replaces the `/profile` placeholder (currently `"Profile page — coming in Step 4"`) with a real,
logged-in-only account page. It shows the signed-in user's identity (name, email, member-since date) and a
small read-only summary of their expense activity (how many expenses they've logged and how much they've
spent in total), pulled from the `expenses` table that already exists and is seeded with demo data. This is
the first page in the app gated behind authentication, and the first place the navbar reacts to whether
someone is signed in.

## Depends on
- Step 1 (Database setup) — `users` and `expenses` tables, `get_db()`.
- Step 2 (Registration) — `session["user_id"]` is set on signup, so a session exists to test against.

## Routes
- `GET /profile` — modify the existing placeholder. If `session["user_id"]` is missing, redirect to
  `/login`. Otherwise look up the user and their expense summary and render `profile.html` — logged-in only.

## Database changes
No new tables or columns. Add two read-only helper functions to `database/db.py`:
- `get_user_by_id(user_id)` — parameterized `SELECT` on `users` by `id`; returns the row (or `None`).
- `get_expense_summary(user_id)` — parameterized query returning the count of expenses and `SUM(amount)`
  for that user (`0`/`0.0` when they have none — use `COALESCE`).

## Templates
- **Create:** `templates/profile.html` — extends `base.html`. Shows name, email, "Member since <date>"
  (formatted from `created_at`), and a small stats row (expense count, total spent).
- **Modify:** `templates/base.html` — the navbar's `nav-links` block currently always shows "Sign in" /
  "Get started". Change it to show a "Profile" link (and no sign in/get started links) when
  `session.user_id` is present, keeping the current links for anonymous visitors.

## Files to change
- `app.py` — rewrite the `/profile` route: session check + redirect, fetch user + summary, render template.
- `database/db.py` — add `get_user_by_id` and `get_expense_summary`.
- `templates/base.html` — conditional navbar links based on `session.user_id`.

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs.
- Parameterised queries only.
- Passwords are never touched or displayed on this page (`password_hash` is not passed to the template).
- Use CSS variables — never hardcode hex values.
- All templates extend `base.html`.
- Anonymous access to `/profile` must redirect, never render, error, or leak user data.

## Definition of done
- [ ] Visiting `/profile` with no active session redirects to `/login`.
- [ ] Registering a new account and then visiting `/profile` shows that account's name and email.
- [ ] The "Member since" date matches the user's `created_at` value.
- [ ] The expense summary shown matches the actual count/sum of rows in `expenses` for that user (verify
      against the demo user's 8 seeded expenses).
- [ ] A user with zero expenses sees a count of 0 and a total of 0, not an error.
- [ ] The navbar shows a "Profile" link (not "Sign in"/"Get started") while logged in.
- [ ] App starts and runs without errors (`./venv/Scripts/python.exe app.py`).
