import sqlite3
import json
from datetime import date, datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "aitrainer.db"


def get_conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                username    TEXT PRIMARY KEY,
                xp          INTEGER DEFAULT 0,
                level       INTEGER DEFAULT 1,
                created_at  TEXT DEFAULT (datetime('now')),
                last_active TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS submissions (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                username     TEXT NOT NULL,
                challenge_id TEXT NOT NULL,
                prompt       TEXT NOT NULL,
                response     TEXT NOT NULL,
                score        INTEGER NOT NULL,
                xp_earned    INTEGER NOT NULL,
                feedback     TEXT,
                created_at   TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (username) REFERENCES users(username)
            );

            CREATE TABLE IF NOT EXISTS user_badges (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                username   TEXT NOT NULL,
                badge_id   TEXT NOT NULL,
                earned_at  TEXT DEFAULT (datetime('now')),
                UNIQUE(username, badge_id),
                FOREIGN KEY (username) REFERENCES users(username)
            );
        """)


def get_or_create_user(username: str) -> dict:
    with get_conn() as conn:
        conn.execute("""
            INSERT OR IGNORE INTO users (username) VALUES (?)
        """, (username,))
        conn.execute("""
            UPDATE users SET last_active = datetime('now') WHERE username = ?
        """, (username,))
        row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        badges = conn.execute(
            "SELECT badge_id, earned_at FROM user_badges WHERE username = ?", (username,)
        ).fetchall()
        completions = conn.execute("""
            SELECT challenge_id, MAX(score) as best_score
            FROM submissions WHERE username = ?
            GROUP BY challenge_id
        """, (username,)).fetchall()
    return _build_user_dict(row, badges, completions)


def get_user(username: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if not row:
            return None
        badges = conn.execute(
            "SELECT badge_id, earned_at FROM user_badges WHERE username = ?", (username,)
        ).fetchall()
        completions = conn.execute("""
            SELECT challenge_id, MAX(score) as best_score
            FROM submissions WHERE username = ?
            GROUP BY challenge_id
        """, (username,)).fetchall()
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
        "badges": [{"badge_id": b["badge_id"], "earned_at": b["earned_at"]} for b in badges],
        "completions": {c["challenge_id"]: c["best_score"] for c in completions},
    }


def add_xp(username: str, xp: int):
    from challenges import get_level
    with get_conn() as conn:
        conn.execute("UPDATE users SET xp = xp + ? WHERE username = ?", (xp, username))
        new_xp = conn.execute("SELECT xp FROM users WHERE username = ?", (username,)).fetchone()["xp"]
        new_level = get_level(new_xp)["level"]
        conn.execute("UPDATE users SET level = ? WHERE username = ?", (new_level, username))


def add_submission(username: str, challenge_id: str, prompt: str,
                   response: str, score: int, xp_earned: int, feedback: str) -> int:
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO submissions (username, challenge_id, prompt, response, score, xp_earned, feedback)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, challenge_id, prompt, response, score, xp_earned, feedback))
        return cur.lastrowid


def check_and_award_badges(username: str) -> list[str]:
    from challenges import BADGES, CHALLENGES
    from copilot_challenges import COPILOT_CHALLENGES, COPILOT_BADGES
    with get_conn() as conn:
        existing = {r["badge_id"] for r in conn.execute(
            "SELECT badge_id FROM user_badges WHERE username = ?", (username,)
        ).fetchall()}

        completions = {r["challenge_id"]: r["best_score"] for r in conn.execute("""
            SELECT challenge_id, MAX(score) as best_score
            FROM submissions WHERE username = ?
            GROUP BY challenge_id
        """, (username,)).fetchall()}

        today_count = conn.execute("""
            SELECT COUNT(DISTINCT challenge_id) as cnt
            FROM submissions
            WHERE username = ? AND date(created_at) = date('now')
        """, (username,)).fetchone()["cnt"]

        high_scores = conn.execute("""
            SELECT COUNT(DISTINCT challenge_id) as cnt
            FROM (
                SELECT challenge_id, MAX(score) as best
                FROM submissions WHERE username = ?
                GROUP BY challenge_id
                HAVING best >= 80
            )
        """, (username,)).fetchone()["cnt"]

    new_badges = []

    def award(badge_id: str):
        if badge_id not in existing:
            with get_conn() as conn:
                try:
                    conn.execute(
                        "INSERT INTO user_badges (username, badge_id) VALUES (?, ?)",
                        (username, badge_id)
                    )
                    new_badges.append(badge_id)
                    existing.add(badge_id)
                except sqlite3.IntegrityError:
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
    with get_conn() as conn:
        rows = conn.execute("""
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
            LIMIT ?
        """, (limit,)).fetchall()
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
    with get_conn() as conn:
        if challenge_id:
            rows = conn.execute("""
                SELECT * FROM submissions WHERE username = ? AND challenge_id = ?
                ORDER BY created_at DESC LIMIT 5
            """, (username, challenge_id)).fetchall()
        else:
            rows = conn.execute("""
                SELECT * FROM submissions WHERE username = ?
                ORDER BY created_at DESC LIMIT 20
            """, (username,)).fetchall()
    return [dict(r) for r in rows]
