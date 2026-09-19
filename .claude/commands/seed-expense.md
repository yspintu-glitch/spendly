---
description: Seed a new random expense for an existing user into expense_tracker.db
allowed-tools: Bash(./venv/Scripts/python.exe:*), Read
---

## Context

- Database file: `expense_tracker.db` in the repo root, managed by `database/db.py`.
- `expenses` schema (see `database/db.py`):
  - `id INTEGER PRIMARY KEY AUTOINCREMENT`
  - `user_id INTEGER NOT NULL` (FK to `users.id`, `ON DELETE CASCADE`)
  - `amount REAL NOT NULL`
  - `category TEXT NOT NULL`
  - `date TEXT NOT NULL`
  - `description TEXT`
  - `created_at TEXT DEFAULT (datetime('now'))`
- Categories used elsewhere in the app (`seed_db()`): `Food`, `Transport`, `Bills`, `Health`,
  `Entertainment`, `Shopping`, `Other`.

## Task

Insert one new random expense row for an existing user in `expense_tracker.db`, then confirm.

1. **Use the venv Python** at `./venv/Scripts/python.exe` (per CLAUDE.md) for every command below.

2. **Pick a user.** Query existing users and pick one at random (or use the one the user specifies):
   ```
   <venv-python> -c "import sqlite3; c = sqlite3.connect('expense_tracker.db'); print(c.execute('SELECT id, name FROM users').fetchall())"
   ```
   If there are no users yet, tell the user to run `/seed-user` first.

3. **Generate random expense data:**
   - `amount`: a plausible amount, e.g. between 5.00 and 200.00, rounded to 2 decimals.
   - `category`: chosen randomly from `Food`, `Transport`, `Bills`, `Health`, `Entertainment`,
     `Shopping`, `Other`.
   - `date`: a random day within the current month, formatted `YYYY-MM-DD`.
   - `description`: a short plausible description matching the category (e.g. "Grocery run" for
     Food, "Taxi fare" for Transport).

4. **Insert the expense:**
   ```
   <venv-python> -c "
   import sqlite3

   conn = sqlite3.connect('expense_tracker.db')
   conn.execute('PRAGMA foreign_keys = ON')
   conn.execute(
       'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
       (<user_id>, <amount>, '<category>', '<date>', '<description>'),
   )
   conn.commit()
   print('Inserted expense:', conn.execute('SELECT id, user_id, amount, category, date, description FROM expenses WHERE id = last_insert_rowid()').fetchone())
   conn.close()
   "
   ```

5. **Report back** the inserted `id`, `user_id` (and the user's name), `amount`, `category`, `date`,
   and `description`.

## Notes

- Do not hardcode a fixed amount/category/date/description — generate fresh random values each run.
- Do not touch the `users` table or any other data.
- If `expense_tracker.db` doesn't exist yet, run `init_db()` first:
  `<venv-python> -c "from database.db import init_db; init_db()"`.
