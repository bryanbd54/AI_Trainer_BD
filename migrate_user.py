#!/usr/bin/env python3
"""Migrate a user's username and display name."""
import sys
import database as db


def migrate_user(old_username: str, new_username: str, new_display_name: str | None = None):
    """
    Migrate a user's username and optionally display name.
    
    This updates the username in the users table and all foreign key references
    in submissions and user_badges tables.
    """
    old_username = old_username.strip().lower()
    new_username = new_username.strip().lower()
    new_display_name = new_display_name or new_username
    
    conn = db.get_conn()
    try:
        with conn:
            with conn.cursor() as cur:
                # Check if old user exists
                cur.execute("SELECT id FROM users WHERE username = %s", (old_username,))
                if not cur.fetchone():
                    print(f"✗ User '{old_username}' not found", file=sys.stderr)
                    sys.exit(1)
                
                # Check if new username already exists
                cur.execute("SELECT id FROM users WHERE username = %s", (new_username,))
                if cur.fetchone():
                    print(f"✗ Username '{new_username}' already exists", file=sys.stderr)
                    sys.exit(1)
                
                # Update submissions
                cur.execute(
                    "UPDATE submissions SET username = %s WHERE username = %s",
                    (new_username, old_username)
                )
                
                # Update user_badges
                cur.execute(
                    "UPDATE user_badges SET username = %s WHERE username = %s",
                    (new_username, old_username)
                )
                
                # Update users table
                cur.execute(
                    "UPDATE users SET username = %s, display_name = %s WHERE username = %s",
                    (new_username, new_display_name, old_username)
                )
                
                print(f"✓ Migrated '{old_username}' → '{new_username}'")
                print(f"✓ Display name set to '{new_display_name}'")
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python migrate_user.py <old_username> <new_username> [new_display_name]", file=sys.stderr)
        sys.exit(1)
    
    old_username = sys.argv[1]
    new_username = sys.argv[2]
    new_display_name = sys.argv[3] if len(sys.argv) > 3 else new_username
    
    migrate_user(old_username, new_username, new_display_name)

