#!/usr/bin/env python3
"""Simple admin management script."""
import sys
import database as db


def make_admin(username: str):
    """Make a user an admin."""
    try:
        db.update_user_permissions(username.strip().lower(), None, True)
        print(f"✓ {username} is now an admin")
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python manage.py <username>", file=sys.stderr)
        sys.exit(1)
    make_admin(sys.argv[1])

