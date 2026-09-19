---
description: Seed a new random Indian-named user into expense_tracker.db
allowed-tools: Bash(./venv/Scripts/python.exe:*), Read
---

## Context

- Database file: `expense_tracker.db` in the repo root, managed by `database/db.py`.
- `users` schema (see `database/db.py`):
  - `id INTEGER PRIMARY KEY AUTOINCREMENT`
  - `name TEXT NOT NULL`
  - `email TEXT UNIQUE NOT NULL`
  - `password_hash TEXT NOT NULL`
  - `created_at TEXT DEFAULT (datetime('now'))`
- The only enforced uniqueness constraint is on `email`. Password hashes are generated with
  `werkzeug.security.generate_password_hash`, exactly like `seed_db()` does for the demo user.

## Task

Create one new user in `expense_tracker.db` with a randomly chosen Indian name, guaranteeing the
generated email is unique, then insert it and confirm.

1. **Pick a random Indian name.** Choose a first name and a last name from a broad pool of common
   Indian given/family names (mix of regions — e.g. Aarav, Vivaan, Aditi, Priya, Rohan, Ishaan,
   Ananya, Kavya, Arjun, Meera, Rajesh, Sanjay, Deepika, Neha, Karthik, Lakshmi, Nair, Sharma,
   Verma, Iyer, Reddy, Gupta, Patel, Singh, Menon, Rao, Chatterjee, Bhat, Joshi, Kulkarni). Combine
   them into a full `name` (e.g. "Ishaan Verma").

2. **Derive a candidate email** from the name, e.g. `firstname.lastname@example.com` (lowercase,
   no spaces/diacritics).

3. **Use the venv Python** at `./venv/Scripts/python.exe` (per CLAUDE.md) for every command below.

4. **Guarantee uniqueness.** Query the existing `users` table for that email (and, to be safe,
   for an exact `name` collision too):
   ```
   <venv-python> -c "import sqlite3; c = sqlite3.connect('expense_tracker.db'); print(c.execute('SELECT name, email FROM users').fetchall())"
   ```
   If the candidate email (or name) already exists, pick a new random name (or append a numeric
   suffix to the email, e.g. `firstname.lastname2@example.com`) and re-check until it's unique.

5. **Insert the user.** Use the venv Python so `werkzeug.security.generate_password_hash` is
   available, matching the hashing already used in `seed_db()`. Use a default password of
   `demo123` unless the user asks for a different one:
   ```
   <venv-python> -c "
   import sqlite3
   from werkzeug.security import generate_password_hash

   conn = sqlite3.connect('expense_tracker.db')
   conn.execute('PRAGMA foreign_keys = ON')
   password_hash = generate_password_hash('demo123')
   conn.execute(
       'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
       ('<Full Name>', '<unique.email@example.com>', password_hash),
   )
   conn.commit()
   print('Inserted user:', conn.execute('SELECT id, name, email, created_at FROM users WHERE email = ?', ('<unique.email@example.com>',)).fetchone())
   conn.close()
   "
   ```

6. **Report back** the inserted `id`, `name`, `email`, and the password used, so the user can log
   in for testing.

## Notes

- Do not hardcode a fixed name/email — generate a fresh random Indian name each time this command
  runs, and always re-verify uniqueness against the current contents of the table before inserting.
- Do not touch the `expenses` table or any other data.
- If `expense_tracker.db` doesn't exist yet, run `init_db()` first:
  `<venv-python> -c "from database.db import init_db; init_db()"`.
