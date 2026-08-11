# MLB Team Lookup (CLI) — simple auth + team DB

This small Python CLI requires a user to register or login, then asks for an MLB team name and returns the division and biggest rivals.

Requirements
- Python 3.8+
- Install dependencies:
  python -m pip install -r requirements.txt

Run
- python app.py

Behavior
- On first run the app creates a local SQLite database `app.db` and seeds 30 MLB teams.
- Register a user (or register a test user).
- Login and enter a team name (case-insensitive). If the team isn't found exactly, fuzzy suggestions are offered.

Notes
- Passwords are hashed with bcrypt.
- This is a simple educational prototype — do not use it as-is for production authentication.