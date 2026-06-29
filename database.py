import os
import json
from datetime import date, datetime
from contextlib import contextmanager

import psycopg2
import psycopg2.extras


def get_conn():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    return conn


@contextmanager
def _cursor(conn):
    """Yield a RealDictCursor and commit/rollback on exit."""
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def init_db():
    conn = get_conn()
    with _cursor(conn) as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username    TEXT PRIMARY KEY,
                xp          INTEGER DEFAULT 0,
                level       INTEGER DEFAULT 1,
                created_at  TIMESTAMPTZ DEFAULT NOW(),
                last_active TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id           SERIAL PRIMARY KEY,
                username     TEXT NOT NULL,
                challenge_id TEXT NOT NULL,
                prompt       TEXT NOT NULL,
                response     TEXT NOT NULL,
                score        INTEGER NOT NULL,
                xp_earned    INTEGER NOT NULL,
                feedback     TEXT,
                created_at   TIMESTAMPTZ DEFAULT NOW(),
                FOREIGN KEY (username) REFERENCES users(username)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_badges (
                id         SERIAL PRIMARY KEY,
                username   TEXT NOT NULL,
                badge_id   TEXT NOT NULL,
                earned_at  TIMESTAMPTZ DEFAULT NOW(),
                UNIQUE(username, badge_id),
                FOREIGN KEY (username) REFERENCES users(username)
            )
        """)


def get_or_create_user(username: str) -> dict:
    conn = get_conn()
    with _cursor(conn) as cur:
        cur.execute("""
            INSERT INTO users (username) VALUES (%s)
            ON CONFLICT (username) DO NOTHING
        """, (username,))
        cur.execute("""
            UPDATE users SET last_active = NOW() WHERE username = %s
        """, (username,))
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        row = cur.fetchone()
        cur.execute(
            "SELECT badge_id, earned_at FROM user_badges WHERE username = %s", (username,)
        )
        badges = cur.fetchall()
        cur.execute("""
            SELECT challenge_id, MAX(score) as best_score
            FROM submissions WHERE username = %s
            GROUP BY challenge_id
        """, (username,))
        completions = cur.fetchall()
    return _build_user_dict(row, badges, completions)


def get_user(username: str) -> dict | None:
    conn = get_conn()
    with _cursor(conn) as cur:
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        row = cur.fetchone()
        if not row:
            return None
        cur.execute(
            "SELECT badge_id, earned_at FROM user_badges WHERE username = %s", (username,)
        )
        badges = cur.fetchall()
        cur.execute("""
            SELECT challenge_id, MAX(score) as best_score
            FROM submissions WHERE username = %s
            GROUP BY challenge_id
        """, (username,))
        completions = cur.fetchall()
    return _build_user_dict(row, badges, completions)


def _build_user_dict(row, badges, completions) -> dict:
    from challenges import get_level, LEVELS
    xp = row["xp"]
    level_info = get_level(xp)
    level_num = level_info["level"]
    next_level = LEVELS[level_num] if level_num < len(LEVELS) else None
    progress_pct = 0
    if next_level:
        span = next_level["min_xp"] - level_info["min_xp"]
        earned = xp - level_info["min_xp"]
        progress_pct = min(100, int((earned / span) * 100))
    return {
        "username": row["username"],
        "xp": xp,
        "level": level_num,
        "level_name": level_info["name"],
        "level_color": level_info["color"],
        "xp_to_next": (next_level["min_xp"] - xp) if next_level else 0,
        "progress_pct": progress_pct,
        "created_at": row["created_at"],
        "last_active": row["last_active"],
        "badges": [{"badge_id": b["badge_id"], "earned_at": str(b["earned_at"])} for b in badges],
        "completions": {c["challenge_id"]: c["best_score"] for c in completions},
    }


def add_xp(username: str, xp: int):
    from challenges import get_level
    conn = get_conn()
    with _cursor(conn) as cur:
        cur.execute("UPDATE users SET xp = xp + %s WHERE username = %s", (xp, username))
        cur.execute("SELECT xp FROM users WHERE username = %s", (username,))
        new_xp = cur.fetchone()["xp"]
        new_level = get_level(new_xp)["level"]
        cur.execute("UPDATE users SET level = %s WHERE username = %s", (new_level, username))


def add_submission(username: str, challenge_id: str, prompt: str,
                   response: str, score: int, xp_earned: int, feedback: str) -> int:
    conn = get_conn()
    with _cursor(conn) as cur:
        cur.execute("""
            INSERT INTO submissions (username, challenge_id, prompt, response, score, xp_earned, feedback)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (username, challenge_id, prompt, response, score, xp_earned, feedback))
        return cur.fetchone()["id"]


def check_and_award_badges(username: str) -> list[str]:
    from challenges import BADGES, CHALLENGES
    from copilot_challenges import COPILOT_CHALLENGES, COPILOT_BADGES
    conn = get_conn()
    with _cursor(conn) as cur:
        cur.execute(
            "SELECT badge_id FROM user_badges WHERE username = %s", (username,)
        )
        existing = {r["badge_id"] for r in cur.fetchall()}

        cur.execute("""
            SELECT challenge_id, MAX(score) as best_score
            FROM submissions WHERE username = %s
            GROUP BY challenge_id
        """, (username,))
        completions = {r["challenge_id"]: r["best_score"] for r in cur.fetchall()}

        cur.execute("""
            SELECT COUNT(DISTINCT challenge_id) as cnt
            FROM submissions
            WHERE username = %s AND created_at::date = CURRENT_DATE
        """, (username,))
        today_count = cur.fetchone()["cnt"]

        cur.execute("""
            SELECT COUNT(DISTINCT challenge_id) as cnt
            FROM (
                SELECT challenge_id, MAX(score) as best
                FROM submissions WHERE username = %s
                GROUP BY challenge_id
                HAVING MAX(score) >= 80
            ) sub
        """, (username,))
        high_scores = cur.fetchone()["cnt"]

    new_badges = []

    def award(badge_id: str):
        if badge_id not in existing:
            conn2 = get_conn()
            with _cursor(conn2) as cur2:
                try:
                    cur2.execute(
                        "INSERT INTO user_badges (username, badge_id) VALUES (%s, %s)",
                        (username, badge_id)
                    )
                    new_badges.append(badge_id)
                    existing.add(badge_id)
                except psycopg2.errors.UniqueViolation:
                    pass

    if completions:
        award("first_challenge")

    jira_ids = {c["id"] for c in CHALLENGES if c["category"] == "jira"}
    if jira_ids.issubset(completions.keys()):
        award("jira_master")

    conf_ids = {c["id"] for c in CHALLENGES if c["category"] == "confluence"}
    if conf_ids.issubset(completions.keys()):
        award("doc_wizard")

    stkh_ids = {c["id"] for c in CHALLENGES if c["category"] == "stakeholder"}
    if stkh_ids.issubset(completions.keys()):
        award("communicator")

    dev_ids = {c["id"] for c in CHALLENGES if c["category"] == "devteam"}
    if dev_ids.issubset(completions.keys()):
        award("team_player")

    req_ids = {c["id"] for c in CHALLENGES if c["category"] == "requirements"}
    if req_ids.issubset(completions.keys()):
        award("requirements_pro")

    if any(s >= 95 for s in completions.values()):
        award("perfectionist")

    if high_scores >= 5:
        award("high_achiever")

    if today_count >= 3:
        award("speed_demon")

    all_ids = {c["id"] for c in CHALLENGES}
    if all_ids.issubset(completions.keys()):
        award("completionist")

    # ── Copilot track badges ───────────────────────────────────────────────────
    copilot_completions = {cid: s for cid, s in completions.items() if cid.startswith("copilot_")}

    if copilot_completions:
        award("copilot_first_challenge")

    for category, badge_id in [
        ("outlook",     "copilot_outlook_master"),
        ("teams",       "copilot_teams_navigator"),
        ("word",        "copilot_word_master"),
        ("excel",       "copilot_excel_analyst"),
        ("powerpoint",  "copilot_ppt_presenter"),
    ]:
        cat_ids = {c["id"] for c in COPILOT_CHALLENGES if c["category"] == category}
        if cat_ids.issubset(copilot_completions.keys()):
            award(badge_id)

    if copilot_completions.get("copilot_ppt_framework_mastery", 0) >= 90:
        award("copilot_framework_expert")

    if any(s >= 95 for s in copilot_completions.values()):
        award("copilot_perfectionist")

    copilot_high = sum(1 for s in copilot_completions.values() if s >= 80)
    if copilot_high >= 5:
        award("copilot_high_achiever")

    all_copilot_ids = {c["id"] for c in COPILOT_CHALLENGES}
    if all_copilot_ids.issubset(copilot_completions.keys()):
        award("copilot_completionist")

    return new_badges


def get_leaderboard(limit: int = 10) -> list[dict]:
    from challenges import get_level
    conn = get_conn()
    with _cursor(conn) as cur:
        cur.execute("""
            SELECT u.username, u.xp, u.level,
                   COUNT(DISTINCT s.challenge_id) as challenges_completed,
                   COALESCE(AVG(best.best_score), 0) as avg_score
            FROM users u
            LEFT JOIN (
                SELECT username, challenge_id, MAX(score) as best_score
                FROM submissions
                GROUP BY username, challenge_id
            ) best ON u.username = best.username
            LEFT JOIN submissions s ON u.username = s.username
            GROUP BY u.username
            ORDER BY u.xp DESC
            LIMIT %s
        """, (limit,))
        rows = cur.fetchall()
    result = []
    for i, r in enumerate(rows):
        level_info = get_level(r["xp"])
        result.append({
            "rank": i + 1,
            "username": r["username"],
            "xp": r["xp"],
            "level": r["level"],
            "level_name": level_info["name"],
            "level_color": level_info["color"],
            "challenges_completed": r["challenges_completed"],
            "avg_score": round(r["avg_score"], 1),
        })
    return result


def get_user_submissions(username: str, challenge_id: str | None = None) -> list[dict]:
    conn = get_conn()
    with _cursor(conn) as cur:
        if challenge_id:
            cur.execute("""
                SELECT * FROM submissions WHERE username = %s AND challenge_id = %s
                ORDER BY created_at DESC LIMIT 5
            """, (username, challenge_id))
        else:
            cur.execute("""
                SELECT * FROM submissions WHERE username = %s
                ORDER BY created_at DESC LIMIT 20
            """, (username,))
        rows = cur.fetchall()
    return [dict(r) for r in rows]
