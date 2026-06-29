import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import database as db
from challenges import CHALLENGES, CATEGORIES, BADGES, get_level
from copilot_challenges import COPILOT_CHALLENGES, COPILOT_CATEGORIES, COPILOT_BADGES
from evaluator import evaluate_submission, DEMO_MODE

ALL_CHALLENGES = CHALLENGES + COPILOT_CHALLENGES
ALL_BADGES = {**BADGES, **COPILOT_BADGES}

app = FastAPI(title="Claude AI Trainer")
db.init_db()

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# ── Request Models ────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    display_name: str | None = None

class SubmissionCreate(BaseModel):
    username: str
    prompt: str


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def root():
    with open(os.path.join(static_dir, "index.html")) as f:
        return f.read()


@app.post("/api/register", status_code=201)
async def register_user(user: UserRegister):
    username = user.username.strip()
    email = user.email.strip().lower()
    if not username or len(username) > 30:
        raise HTTPException(400, "Username must be 1-30 characters")
    if not email or "@" not in email:
        raise HTTPException(400, "Valid email required")
    if not user.password or len(user.password) < 6:
        raise HTTPException(400, "Password must be at least 6 characters")
    try:
        return db.create_user(username, email, user.password, user.display_name)
    except Exception as e:
        if "unique" in str(e).lower() or "duplicate" in str(e).lower():
            raise HTTPException(409, "Username or email already taken")
        raise HTTPException(500, "Could not create account")


@app.post("/api/users")
async def login_user(user: UserCreate):
    username = user.username.strip()
    if not username:
        raise HTTPException(400, "Username required")
    result = db.authenticate_user(username, user.password)
    if not result:
        raise HTTPException(401, "Invalid username or password")
    return result


@app.get("/api/users/{username}")
async def get_user(username: str):
    user = db.get_user(username)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@app.get("/api/challenges")
async def list_challenges(track: str = Query(default="claude")):
    if track == "copilot":
        return {
            "challenges": [_serialize_challenge(c) for c in COPILOT_CHALLENGES],
            "categories": COPILOT_CATEGORIES,
            "track": "copilot",
        }
    return {
        "challenges": [_serialize_challenge(c) for c in CHALLENGES],
        "categories": CATEGORIES,
        "track": "claude",
    }


@app.get("/api/challenges/{challenge_id}")
async def get_challenge(challenge_id: str):
    challenge = next((c for c in ALL_CHALLENGES if c["id"] == challenge_id), None)
    if not challenge:
        raise HTTPException(404, "Challenge not found")
    return _serialize_challenge(challenge, full=True)


@app.post("/api/challenges/{challenge_id}/submit")
async def submit_challenge(challenge_id: str, submission: SubmissionCreate):
    challenge = next((c for c in ALL_CHALLENGES if c["id"] == challenge_id), None)
    if not challenge:
        raise HTTPException(404, "Challenge not found")

    username = submission.username.strip()
    if not username:
        raise HTTPException(400, "Username required")

    if not db.get_user(username):
        raise HTTPException(404, "User not found")

    # Evaluate the submission
    result = await evaluate_submission(challenge, submission.prompt)
    score = result["score"]

    # Calculate XP
    from challenges import get_xp_reward
    xp_earned = get_xp_reward(score, challenge["xp_reward"])

    # Save submission
    db.add_submission(
        username=username,
        challenge_id=challenge_id,
        prompt=submission.prompt,
        response=result["claude_response"],
        score=score,
        xp_earned=xp_earned,
        feedback=result.get("feedback", ""),
    )

    # Award XP and check badges
    db.add_xp(username, xp_earned)
    new_badges = db.check_and_award_badges(username)

    # Get updated user
    updated_user = db.get_user(username)

    return {
        **result,
        "xp_earned": xp_earned,
        "new_badges": [
            {**ALL_BADGES[b], "id": b} for b in new_badges if b in ALL_BADGES
        ],
        "user": updated_user,
    }


@app.get("/api/status")
async def get_status():
    return {"demo_mode": DEMO_MODE}


@app.get("/api/leaderboard")
async def get_leaderboard():
    return db.get_leaderboard(limit=15)


@app.get("/api/users/{username}/history")
async def get_history(username: str, challenge_id: str | None = None):
    user = db.get_user(username)
    if not user:
        raise HTTPException(404, "User not found")
    return db.get_user_submissions(username, challenge_id)


@app.get("/api/badges")
async def get_badges(track: str = Query(default="claude")):
    if track == "copilot":
        return COPILOT_BADGES
    return BADGES


# ── Helpers ───────────────────────────────────────────────────────────────────

def _serialize_challenge(c: dict, full: bool = False) -> dict:
    base = {
        "id": c["id"],
        "track": c.get("track", "claude"),
        "category": c["category"],
        "category_label": c["category_label"],
        "icon": c["icon"],
        "title": c["title"],
        "difficulty": c["difficulty"],
        "xp_reward": c["xp_reward"],
        "scenario": c["scenario"],
    }
    if full:
        base.update({
            "context": c["context"],
            "what_makes_a_great_prompt": c["what_makes_a_great_prompt"],
            "model_prompt": c["model_prompt"],
        })
    return base


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
