import os
import psycopg2
import psycopg2.extras
from passlib.context import CryptContext

DATABASE_URL = os.environ.get("DATABASE_URL", "")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__truncate_error=False)


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    pass  # schema lives in Railway — see postgres railway.session.sql


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_user(username: str, email: str, password: str, display_name: str | None = None) -> dict:
    conn = get_conn()
    try:
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    INSERT INTO users (username, email, password_hash, display_name)
                    VALUES (%s, %s, %s, %s)
                    RETURNING *
                """, (username.strip(), email.strip().lower(), hash_password(password), display_name or username))
                row = dict(cur.fetchone())
    finally:
        conn.close()
    return _build_user_dict(row, [], [])


def authenticate_user(username: str, password: str) -> dict | None:
    conn = get_conn()
    try:
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT * FROM users WHERE username = %s", (username.strip(),))
                row = cur.fetchone()
                if not row or not verify_password(password, row["password_hash"]):
                    return None
                row = dict(row)
                cur.execute("UPDATE users SET last_active = NOW() WHERE username = %s", (username,))
                cur.execute("SELECT badge_id, earned_at FROM user_badges WHERE username = %s", (username,))
                badges = cur.fetchall()
                cur.execute("""
                    SELECT challenge_id, MAX(score) as best_score
                    FROM submissions WHERE username = %s
                    GROUP BY challenge_id
                """, (username,))
                completions = cur.fetchall()
    finally:
        conn.close()
    return _build_user_dict(row, badges, completions)


def get_user(username: str) -> dict | None:
    conn = get_conn()
    try:
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT * FROM users WHERE username = %s", (username,))
                row = cur.fetchone()
                if not row:
                    return None
                row = dict(row)
                cur.execute("SELECT badge_id, earned_at FROM user_badges WHERE username = %s", (username,))
                badges = cur.fetchall()
                cur.execute("""
                    SELECT challenge_id, MAX(score) as best_score
                    FROM submissions WHERE username = %s
                    GROUP BY challenge_id
                """, (username,))
                completions = cur.fetchall()
    finally:
        conn.close()
    return _build_user_dict(row, badges, completions)


def _build_user_dict(row: dict, badges, completions) -> dict:
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
        "display_name": row.get("display_name") or row["username"],
        "email": row.get("email", ""),
        "xp": xp,
        "level": level_num,
        "level_name": level_info["name"],
        "level_color": level_info["color"],
        "xp_to_next": (next_level["min_xp"] - xp) if next_level else 0,
        "progress_pct": progress_pct,
        "created_at": str(row["created_at"]),
        "last_active": str(row["last_active"]),
        "badges": [{"badge_id": b["badge_id"], "earned_at": str(b["earned_at"])} for b in badges],
        "completions": {c["challenge_id"]: c["best_score"] for c in completions},
    }


def add_xp(username: str, xp: int):
    from challenges import get_level
    conn = get_conn()
    try:
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("UPDATE users SET xp = xp + %s WHERE username = %s RETURNING xp", (xp, username))
                new_xp = cur.fetchone()["xp"]
                new_level = get_level(new_xp)["level"]
                cur.execute("UPDATE users SET level = %s WHERE username = %s", (new_level, username))
    finally:
        conn.close()


def add_submission(username: str, challenge_id: str, prompt: str,
                   response: str, score: int, xp_earned: int, feedback: str) -> int:
    conn = get_conn()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO submissions (username, challenge_id, prompt, response, score, xp_earned, feedback)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (username, challenge_id, prompt, response, score, xp_earned, feedback))
                return cur.fetchone()[0]
    finally:
        conn.close()


def check_and_award_badges(username: str) -> list[str]:
    from challenges import BADGES, CHALLENGES
    from copilot_challenges import COPILOT_CHALLENGES, COPILOT_BADGES

    conn = get_conn()
    try:
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT badge_id FROM user_badges WHERE username = %s", (username,))
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
                    ) t
                """, (username,))
                high_scores = cur.fetchone()["cnt"]

                to_award = []

                def maybe_award(badge_id: str):
                    if badge_id not in existing:
                        to_award.append(badge_id)
                        existing.add(badge_id)

                if completions:
                    maybe_award("first_challenge")

                jira_ids = {c["id"] for c in CHALLENGES if c["category"] == "jira"}
                if jira_ids.issubset(completions.keys()):
                    maybe_award("jira_master")

                conf_ids = {c["id"] for c in CHALLENGES if c["category"] == "confluence"}
                if conf_ids.issubset(completions.keys()):
                    maybe_award("doc_wizard")

                stkh_ids = {c["id"] for c in CHALLENGES if c["category"] == "stakeholder"}
                if stkh_ids.issubset(completions.keys()):
                    maybe_award("communicator")

                dev_ids = {c["id"] for c in CHALLENGES if c["category"] == "devteam"}
                if dev_ids.issubset(completions.keys()):
                    maybe_award("team_player")

                req_ids = {c["id"] for c in CHALLENGES if c["category"] == "requirements"}
                if req_ids.issubset(completions.keys()):
                    maybe_award("requirements_pro")

                if any(s >= 95 for s in completions.values()):
                    maybe_award("perfectionist")

                if high_scores >= 5:
                    maybe_award("high_achiever")

                if today_count >= 3:
                    maybe_award("speed_demon")

                all_ids = {c["id"] for c in CHALLENGES}
                if all_ids.issubset(completions.keys()):
                    maybe_award("completionist")

                copilot_completions = {cid: s for cid, s in completions.items() if cid.startswith("copilot_")}

                if copilot_completions:
                    maybe_award("copilot_first_challenge")

                for category, badge_id in [
                    ("outlook",    "copilot_outlook_master"),
                    ("teams",      "copilot_teams_navigator"),
                    ("word",       "copilot_word_master"),
                    ("excel",      "copilot_excel_analyst"),
                    ("powerpoint", "copilot_ppt_presenter"),
                ]:
                    cat_ids = {c["id"] for c in COPILOT_CHALLENGES if c["category"] == category}
                    if cat_ids.issubset(copilot_completions.keys()):
                        maybe_award(badge_id)

                if copilot_completions.get("copilot_ppt_framework_mastery", 0) >= 90:
                    maybe_award("copilot_framework_expert")

                if any(s >= 95 for s in copilot_completions.values()):
                    maybe_award("copilot_perfectionist")

                if sum(1 for s in copilot_completions.values() if s >= 80) >= 5:
                    maybe_award("copilot_high_achiever")

                all_copilot_ids = {c["id"] for c in COPILOT_CHALLENGES}
                if all_copilot_ids.issubset(copilot_completions.keys()):
                    maybe_award("copilot_completionist")

                new_badges = []
                for badge_id in to_award:
                    cur.execute(
                        "INSERT INTO user_badges (username, badge_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                        (username, badge_id)
                    )
                    if cur.rowcount > 0:
                        new_badges.append(badge_id)
    finally:
        conn.close()

    return new_badges


def get_leaderboard(limit: int = 15) -> list[dict]:
    from challenges import get_level
    conn = get_conn()
    try:
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT u.username, u.display_name, u.xp, u.level,
                           COUNT(DISTINCT s.challenge_id) as challenges_completed,
                           COALESCE(AVG(best.best_score), 0) as avg_score
                    FROM users u
                    LEFT JOIN (
                        SELECT username, challenge_id, MAX(score) as best_score
                        FROM submissions
                        GROUP BY username, challenge_id
                    ) best ON u.username = best.username
                    LEFT JOIN submissions s ON u.username = s.username
                    GROUP BY u.username, u.display_name, u.xp, u.level
                    ORDER BY u.xp DESC
                    LIMIT %s
                """, (limit,))
                rows = cur.fetchall()
    finally:
        conn.close()

    result = []
    for i, r in enumerate(rows):
        level_info = get_level(r["xp"])
        result.append({
            "rank": i + 1,
            "username": r["username"],
            "display_name": r["display_name"] or r["username"],
            "xp": r["xp"],
            "level": r["level"],
            "level_name": level_info["name"],
            "level_color": level_info["color"],
            "challenges_completed": r["challenges_completed"],
            "avg_score": round(float(r["avg_score"]), 1),
        })
    return result


def get_user_submissions(username: str, challenge_id: str | None = None) -> list[dict]:
    conn = get_conn()
    try:
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
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
    finally:
        conn.close()
    return [dict(r) for r in rows]
