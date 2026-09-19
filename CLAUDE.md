# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

**Spendly** is a Flask-based personal expense tracking web application built as a progressive learning project. Users can log expenses, view spending patterns, and manage their finances. The project is structured in steps, with database functionality and core features to be implemented progressively.

**Tech stack:**
- **Backend:** Python 3.13 with Flask 3.1.3
- **Frontend:** Vanilla HTML/CSS/JavaScript (no frameworks)
- **Templates:** Jinja2 with template inheritance
- **Database:** SQLite (to be implemented in database/db.py)
- **Testing:** pytest with pytest-flask

## Environment setup

- A `venv` (Python 3.13) already exists in the repo root. Activate it or invoke it directly:
  - Windows: `./venv/Scripts/python.exe` or `./venv/Scripts/activate.ps1`
  - macOS/Linux: `source venv/bin/activate` or `./venv/bin/python`
- Dependencies are listed in `requirements.txt` (`flask`, `werkzeug`, `pytest`, `pytest-flask`) and installed into `venv`
- Install/update with: `./venv/Scripts/python.exe -m pip install -r requirements.txt`

## Running the application

```
./venv/Scripts/python.exe app.py
```

The app will start on `http://localhost:5001` (configured in `app.py`). Use `debug=True` for development.

## Project structure

```
expense-tracker/
├── app.py                 # Flask application and route definitions
├── database/
│   ├── __init__.py
│   └── db.py             # Database setup (students will implement)
├── static/
│   ├── css/
│   │   └── style.css     # Global styles with design system variables
│   └── js/
│       └── main.js       # Shared frontend JavaScript (minimal so far)
├── templates/
│   ├── base.html         # Base template with navbar and footer
│   ├── landing.html      # Landing page with hero and features
│   ├── terms.html        # Terms and Conditions page
│   ├── privacy.html      # Privacy Policy page
│   ├── login.html        # Login page (auth placeholder)
│   └── register.html     # Registration page (auth placeholder)
├── requirements.txt
└── venv/                  # Python virtual environment
```

## Key architecture patterns

### Route organization (app.py)

Routes are organized by section with comment dividers:
- **Public routes** (landing, login, register, terms, privacy)
- **Placeholder routes** (logout, profile, add_expense, edit_expense, delete_expense) — to be implemented in future steps

Each route returns a rendered Jinja2 template. The pattern is simple and intentionally minimal for learning.

### Template inheritance (Jinja2)

All pages extend `base.html`, which provides:
- Sticky navbar with branding and navigation links
- Main content block
- Footer with links and branding

Pages override `{% block content %}` and optionally `{% block head %}` (for custom styles), `{% block scripts %}` (for page-specific JavaScript).

**Example:**
```html
{% extends "base.html" %}
{% block title %}Page Title — Spendly{% endblock %}
{% block content %}
  <!-- page content here -->
{% endblock %}
{% block scripts %}
  <script>
    // page-specific JS
  </script>
{% endblock %}
```

### Design system (CSS)

`style.css` defines a comprehensive design system using CSS custom properties (variables) at `:root`:

**Colors:**
- `--ink`, `--ink-soft`, `--ink-muted`, `--ink-faint` — text colors (grayscale)
- `--paper`, `--paper-warm`, `--paper-card` — backgrounds
- `--accent`, `--accent-light` — primary green color and light variant
- `--accent-2`, `--accent-2-light` — secondary orange color
- `--danger`, `--danger-light` — red for alerts
- `--border`, `--border-soft` — border colors

**Typography:**
- `--font-display` — DM Serif Display (headings)
- `--font-body` — DM Sans (body text)

**Spacing & sizing:**
- `--max-width` — max container width (1200px)
- `--auth-width` — auth form width (440px)
- `--radius-sm/md/lg` — border radius values

Sections already styled: hero, features, CTA, auth pages, footer, content pages (terms/privacy), modal.

### Frontend JavaScript

Minimal vanilla JavaScript, no frameworks. Currently used for:
- Modal interaction (video modal on landing page)
- Video iframe management (clearing src on close to stop playback)

All JavaScript is inline in `{% block scripts %}` within templates since the project has no build system.

## Database setup (in progress)

Students will implement `database/db.py` with:
- `get_db()` — returns SQLite connection with row_factory and foreign keys enabled
- `init_db()` — creates tables with CREATE TABLE IF NOT EXISTS
- `seed_db()` — inserts sample data for development

The database module will be imported and used by route handlers for expense CRUD operations.

## Common development tasks

### Add a new page

1. Create a new route in `app.py` (below existing public routes, before placeholder routes)
2. Create a template in `templates/page-name.html` that extends `base.html`
3. Update navigation links in `base.html` if needed

### Add a new form or interactive feature

Use vanilla JavaScript within a `{% block scripts %}` section. Examples on landing.html (video modal).

### Update styling

Edit `style.css`. Add new component styles after existing sections, before responsive media queries. Use CSS variables for colors and sizing.

### Debug the app

- Use `print()` in route handlers; output appears in Flask's terminal
- Use `console.log()` in JavaScript; view in browser DevTools
- Flask's debug mode shows stack traces on errors

### Run with a specific port

Change the port in the last line of `app.py`:
```python
if __name__ == "__main__":
    app.run(debug=True, port=YOUR_PORT)
```

## Important notes

- The project structure encourages progressive implementation — stub routes and incomplete modules are intentional placeholders for students to fill in
- No external JavaScript libraries (jQuery, Vue, React) — keep frontend vanilla
- Template changes should preserve the Jinja2 block structure so child templates can override sections
- When adding new routes, follow the existing naming pattern (`@app.route("/path")` with `def path_name():`)
