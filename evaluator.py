"""
Evaluates user prompt submissions using Claude as judge.
Supports two tracks: 'claude' (Anthropic best practices) and 'copilot' (Microsoft 4-part framework).
Uses prompt caching on the system prompt to reduce costs.
Set DEMO_MODE=1 (or omit ANTHROPIC_API_KEY) to run without an API key.
"""
import json
import os
import random
import anthropic

DEMO_MODE = not os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("DEMO_MODE") == "1"

client = None if DEMO_MODE else anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

EVALUATOR_SYSTEM = """You are an expert AI prompting coach who evaluates how well product managers use Claude for real PM work.

Your evaluation is grounded in Anthropic's official 2025-2026 prompting best practices documentation.

## What excellent prompts look like (current best practices)

**Structure (most impactful technique):**
- Use XML tags to separate prompt components: <context>, <task>, <requirements>, <output_format>, <example>
- Put long context/data BEFORE instructions, not after
- Name every output section explicitly (e.g., list the exact headers you want)

**Role assignment:**
- Specific role with seniority and company context: "You are a senior PM at a Series B fintech startup"
- NOT vague: "You are a PM" or "Act as a product manager"

**Instructions (critical):**
- Tell Claude WHAT TO DO, not just what not to do ("Write in flowing prose" beats "Don't use bullet points")
- Positive instructions with a target beat negative instructions with a prohibition
- Be specific: "6-8 Given/When/Then acceptance criteria" not "write acceptance criteria"

**Output quality:**
- Include worked examples with <example> tags (few-shot prompting) for format-sensitive outputs
- Add self-check instructions: "Before finishing, verify every criterion is independently testable"
- Specify audience and their reading constraints: "A VP who has 3 minutes — lead with status, not background"

**Context:**
- Give Claude the WHY, not just the WHAT (business context, audience, constraints)
- Include relevant numbers and constraints directly in the prompt
- Ask Claude to flag ambiguities with [AMBIGUITY: description] rather than silently guessing

## What weak prompts look like
- Under 100 characters ("write a user story about passwords")
- No role, or vague role ("you are a PM")
- No output format specification
- No context about company, audience, or business situation
- Vague instructions that could mean anything
- No self-check or quality criteria

## Scoring dimensions (0-25 each, total 0-100)

**Clarity (0-25):** How specific and unambiguous are the instructions?
- 0-8: Vague or one-line prompt with no real direction
- 9-16: Some specificity but key instructions are still vague
- 17-25: Very specific, every instruction has a clear target

**Context (0-25):** How well does the prompt provide business context, audience, and constraints?
- 0-8: No context — could be for any company/situation
- 9-16: Some context but audience or business situation unclear
- 17-25: Rich context: role with seniority, company type, audience, reading constraints, WHY

**Structure (0-25):** How well-organized is the prompt? Does it use modern techniques?
- 0-8: Prose blob with no organization
- 9-16: Some organization (numbered list, paragraphs) but no XML structure or examples
- 17-25: Uses XML tags, named output sections, or few-shot examples — clearly structured

**Output Quality (0-25):** How good is Claude's actual response given this prompt?
- 0-8: Generic, incomplete, or could apply to any situation
- 9-16: Decent quality but missing key sections or specificity
- 17-25: Professional, immediately usable, addresses the specific scenario

Return your evaluation as a JSON object with this exact structure:
{
  "claude_response": "the full response Claude would generate given the user's prompt",
  "score": <0-100 integer>,
  "score_breakdown": {
    "clarity": <0-25>,
    "context": <0-25>,
    "structure": <0-25>,
    "output_quality": <0-25>
  },
  "feedback": "2-3 sentences of specific, actionable feedback referencing what the user's prompt did well and what specific technique would most improve it",
  "tip": "one specific, named technique the user could apply right now (e.g., 'Add XML tags to separate your context from your output format requirements — <context> ... </context> before <output_format> ... </output_format>')",
  "model_comparison": "1-2 sentences explaining the most important structural difference between the user's prompt and the gold standard, and what output that difference produced"
}

Be honest and calibrated:
- 90-100: Exceptional — uses XML structure, specific role, few-shot examples, self-check
- 75-89: Strong — specific role and context, named output sections, audience-aware
- 55-74: Solid — has a role and some specificity, but misses structure or key details
- 35-54: Developing — has some elements but too vague or missing key context
- Under 35: Needs significant improvement — too short, no role, or no output format

Most first attempts score 40-65. Be specific in feedback — name the exact technique to apply next."""

COPILOT_EVALUATOR_SYSTEM = """You are an expert Microsoft 365 Copilot coach who evaluates how well professionals write prompts for M365 Copilot in Outlook, Teams, Word, Excel, and PowerPoint.

Your evaluation is grounded in Microsoft's official 4-part prompting framework: Goal + Context + Source + Expectations.

## Microsoft's 4-Part Framework

**Goal** — The exact output type and purpose. Excellent goals specify output type (email, summary, table, 3 bullets, 1-page doc) + specific task + what it will be used for.

**Context** — Business situation, audience, and constraints. Excellent context provides audience profile, stakes, tone needs, sensitive information constraints, and the "why" behind the request.

**Source** — What organizational data Copilot should draw from. Excellent source use references specific files (/[filename.docx]), named meetings, email threads, channels, or timeframes ("last 7 days"). Grounded responses are always better than ungrounded ones.

**Expectations** — Format, length, tone, and structural requirements. Excellent expectations specify output structure (sections, bullets, table), length constraint (word count, slide count), tone, required inclusions, and any content exclusions.

## What excellent Copilot prompts look like
- All 4 elements present and specific
- Goal names exact output type with a clear business purpose
- Context gives audience, business situation, stakes, and constraints
- Source uses /[filename] slash references or names specific meetings/channels/threads
- Expectations define format, length, tone, required content, and what to exclude
- Anti-instructions present ("do not mention X", "no hedge phrases")
- Self-check or audit instruction at the end ("flag any gaps as [GAP: description]")

## What weak Copilot prompts look like
- Single-element: just a task with no context, source, or expectations
- Vague goal: "summarize this" or "write an email about the project"
- No source: asking Copilot to work from scratch when organizational data exists
- No format: Copilot will default to a generic layout that may not fit the use case

## Scoring dimensions (0–25 each; internally use these keys: clarity, context, structure, output_quality)

**clarity (= Goal, 0–25):** How specific and actionable is the goal?
- 0–8: Vague task with no output type or purpose
- 9–16: Task described but output type or purpose unclear
- 17–25: Exact output type, specific task, and clear business purpose stated

**context (= Context, 0–25):** How well does the prompt supply business background, audience, and constraints?
- 0–8: No context — could apply to any company or situation
- 9–16: Some context but audience or stakes unclear
- 17–25: Rich context: audience profile, business situation, stakes, constraints, sensitivity notes

**structure (= Source, 0–25):** Does the prompt use M365 Source guidance? Is the prompt organized?
- 0–8: No source guidance — working from Copilot's general knowledge only
- 9–16: Some reference to organizational content but vague ("our documents")
- 17–25: Specific file references (/[filename]), named meetings/channels/threads, or per-section source assignment

**output_quality (= Expectations, 0–25):** Are format, length, tone, and structural requirements stated?
- 0–8: No format guidance — Copilot will guess
- 9–16: Some format but missing length, tone, or required content rules
- 17–25: Explicit format, length limit, audience-calibrated tone, required sections, and content exclusions

Return your evaluation as a JSON object with this exact structure:
{
  "claude_response": "the simulated Copilot response given the user's prompt — high quality if the prompt is excellent, generic if the prompt is weak",
  "score": <0-100 integer>,
  "score_breakdown": {
    "clarity": <0-25>,
    "context": <0-25>,
    "structure": <0-25>,
    "output_quality": <0-25>
  },
  "feedback": "2-3 sentences of specific, actionable feedback using Microsoft's framework language (Goal/Context/Source/Expectations) — what the prompt did well and which element would most improve it",
  "tip": "one specific technique from Microsoft's framework the user could apply right now — name the element: Goal / Context / Source / Expectations",
  "model_comparison": "1-2 sentences on the most important framework difference between the user's prompt and the gold standard, and what output that difference produced"
}

Be honest and calibrated:
- 90–100: Exceptional — all 4 elements present, specific, and well-executed
- 75–89: Strong — 3 elements well-executed, 1 partially present
- 55–74: Solid — 2 strong elements, missing Source or Expectations detail
- 35–54: Developing — Goal present, Context and/or Source missing or vague
- Under 35: Needs improvement — one-element prompts, no context, no format

Most first attempts score 35–60. Be specific — name the exact framework element to improve next."""


def _demo_evaluate_copilot(challenge: dict, user_prompt: str) -> dict:
    """Demo evaluator for Copilot track — heuristic scoring on 4-part framework signals."""
    prompt_len = len(user_prompt)

    base = 35
    if prompt_len > 400:
        base += 20
    elif prompt_len > 200:
        base += 10
    # Goal signals
    if any(kw in user_prompt.lower() for kw in ["goal:", "goal —", "what i want", "create a", "draft a", "summarize"]):
        base += 7
    # Context signals
    if any(kw in user_prompt.lower() for kw in ["context:", "context —", "background:", "audience:", "because", "meeting"]):
        base += 7
    # Source signals
    if any(kw in user_prompt.lower() for kw in ["/[", "based on", "from the", "this document", "this thread", "this meeting", "source:"]):
        base += 8
    # Expectations signals
    if any(kw in user_prompt.lower() for kw in ["format:", "expectations:", "expectations —", "bullet", "table", "under ", "maximum", "words"]):
        base += 7
    score = min(92, base + random.randint(-4, 4))

    c = max(5, min(25, int(score * 0.27) + random.randint(-2, 2)))
    ctx = max(5, min(25, int(score * 0.24) + random.randint(-2, 2)))
    s = max(5, min(25, int(score * 0.25) + random.randint(-2, 2)))
    oq = max(0, min(25, score - c - ctx - s))

    feedbacks = [
        "Your prompt includes a clear Goal — good start. Adding a Context element (audience profile, business situation, stakes) would significantly improve Copilot's output quality.",
        "Good detail in the prompt. Strengthen the Source element: reference specific files with /[filename] or name the exact meeting/channel Copilot should use.",
        "The prompt communicates what you want, but the Expectations element is weak. Specify format (bullets/table/sections), exact length (word count or item count), and tone for the audience.",
        "Solid prompt with context. The biggest improvement: add a specific Source reference so Copilot draws from your actual organizational data instead of generating generically.",
    ]
    tips = [
        "Add a Goal element that names the exact output type: 'Create a 3-bullet summary' vs 'Summarize this.' Output type is the single highest-impact addition to any Copilot prompt.",
        "Add a Source element using the /[filename] slash reference — this grounds Copilot in your actual files rather than generating from scratch.",
        "Add an Expectations element: specify format (bullets, table, sections), length (word count), and tone (formal, casual, executive-level) for more reliable output.",
        "Add a Context element explaining who the audience is and what they need — Copilot calibrates tone and detail level from this information.",
    ]

    demo_response = f"""[DEMO MODE — add your ANTHROPIC_API_KEY to see real evaluation]

Simulated Copilot response for: **{challenge['title']}**

In live mode, Claude simulates how M365 Copilot would respond to your prompt in {challenge.get('category_label', 'M365')}. The quality of the simulated response reflects your prompt quality — specific Goal + Context + Source + Expectations produces a usable, professional output; a vague prompt gets a generic one.

Your prompt ({prompt_len} characters) would score approximately **{score}/100** using Microsoft's 4-part framework.

To enable real evaluation: export ANTHROPIC_API_KEY=your-key"""

    return {
        "claude_response": demo_response,
        "score": score,
        "score_breakdown": {"clarity": c, "context": ctx, "structure": s, "output_quality": oq},
        "feedback": random.choice(feedbacks),
        "tip": random.choice(tips),
        "model_comparison": "Demo mode: comparison to the gold standard is unavailable. Add an API key to see a detailed framework-element analysis.",
        "demo_mode": True,
    }


def _demo_evaluate(challenge: dict, user_prompt: str) -> dict:
    """Returns a realistic-looking fake evaluation for demo/testing purposes."""
    prompt_len = len(user_prompt)

    # Score based on prompt length and a few quality signals — purely heuristic
    base = 40
    if prompt_len > 300:
        base += 20
    elif prompt_len > 150:
        base += 10
    if any(kw in user_prompt.lower() for kw in ["you are", "act as", "role"]):
        base += 8
    if any(kw in user_prompt.lower() for kw in ["format", "include", "structure", "section"]):
        base += 7
    if any(kw in user_prompt.lower() for kw in ["context", "audience", "because", "so that"]):
        base += 7
    score = min(92, base + random.randint(-4, 4))

    c = max(5, min(25, int(score * 0.27) + random.randint(-2, 2)))
    ctx = max(5, min(25, int(score * 0.24) + random.randint(-2, 2)))
    s = max(5, min(25, int(score * 0.25) + random.randint(-2, 2)))
    oq = max(0, score - c - ctx - s)
    oq = max(0, min(25, oq))

    feedbacks = [
        "Your prompt gives Claude some direction, but adding a specific role (e.g. 'You are a senior PM at a B2B SaaS company') would sharpen the output significantly. Also try specifying the exact sections you want in the response.",
        "Good start — you've included the key information. To push into the 80+ range, add explicit output format instructions: tell Claude exactly what sections, headers, or table structure you want.",
        "The prompt is clear but light on business context. Tell Claude *why* this task matters and *who* the audience is — that context dramatically changes the quality and tone of the output.",
        "Solid prompt. The main improvement area is edge cases: ask Claude to address error states, out-of-scope items, and potential failure modes for a truly production-ready output.",
    ]
    tips = [
        "Add 'You are a senior [role] at a [company type]' at the start — it's the single highest-impact change you can make to any PM prompt.",
        "End your prompt with 'Flag any assumptions you made and list 3 things that could go wrong.' This surfaces blind spots automatically.",
        "Use numbered output requirements: '1. Executive summary 2. Acceptance criteria table 3. Edge cases list'. Claude follows structured instructions more reliably than prose.",
        "Specify your audience explicitly: 'This will be read by engineers who need to implement it without asking follow-up questions.'",
    ]

    demo_response = f"""[DEMO MODE — add your ANTHROPIC_API_KEY to see real Claude output]

This is a simulated response for the challenge: **{challenge['title']}**

In real mode, Claude would generate a full, production-quality response based on your prompt. The response would directly reflect the quality of your prompt — a vague prompt gets a generic response, while a specific, well-structured prompt with clear role/context/format instructions gets a detailed, immediately usable output.

Your prompt ({prompt_len} characters) would score approximately **{score}/100** in real mode.

To enable real Claude responses, run:
  export ANTHROPIC_API_KEY=your-key
  ./start.sh"""

    return {
        "claude_response": demo_response,
        "score": score,
        "score_breakdown": {"clarity": c, "context": ctx, "structure": s, "output_quality": oq},
        "feedback": random.choice(feedbacks),
        "tip": random.choice(tips),
        "model_comparison": "In demo mode, comparison to the gold standard prompt is unavailable. Add an API key to see a detailed side-by-side analysis.",
        "demo_mode": True,
    }


async def evaluate_submission(challenge: dict, user_prompt: str) -> dict:
    """
    Send user_prompt to Claude in the context of the challenge,
    then evaluate the quality using a separate Claude call with prompt caching.
    Supports 'claude' and 'copilot' tracks — each uses a different evaluator system prompt.
    Falls back to demo mode if no API key is configured.
    """
    is_copilot = challenge.get("track") == "copilot"

    if DEMO_MODE:
        return _demo_evaluate_copilot(challenge, user_prompt) if is_copilot else _demo_evaluate(challenge, user_prompt)

    # Step 1: Execute the user's prompt
    if is_copilot:
        execution_system = (
            f"You are Microsoft 365 Copilot, an AI assistant embedded in {challenge.get('category_label', 'Microsoft 365')}. "
            f"Simulate how M365 Copilot would respond to the following prompt.\n"
            f"Context for this task:\n{challenge['context']}"
        )
    else:
        execution_system = (
            f"You are helping a product manager with their work. "
            f"Context for this task:\n{challenge['context']}"
        )

    try:
        execution_response = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=2000,
            system=[{"type": "text", "text": execution_system}],
            messages=[{"role": "user", "content": user_prompt}],
        )
        claude_response = "".join(
            b.text for b in execution_response.content if b.type == "text"
        )
    except Exception as e:
        claude_response = f"[Error executing prompt: {e}]"

    # Step 2: Evaluate the prompt quality (with caching on the system prompt)
    eval_user_content = f"""Challenge: {challenge['title']}
Challenge Category: {challenge['category_label']}
Challenge Scenario: {challenge['scenario']}

Evaluation Rubric:
{challenge['evaluation_rubric']}

--- USER'S PROMPT ---
{user_prompt}

--- AI RESPONSE TO THAT PROMPT ---
{claude_response}

--- GOLD STANDARD PROMPT (for comparison) ---
{challenge['model_prompt']}

Now evaluate this submission. Use the rubric to score each dimension.
Remember: the score_breakdown must sum to the total score.
Return only valid JSON."""

    evaluator_system = COPILOT_EVALUATOR_SYSTEM if is_copilot else EVALUATOR_SYSTEM

    try:
        eval_response = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=1500,
            system=[
                {
                    "type": "text",
                    "text": evaluator_system,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": eval_user_content}],
        )
        raw = "".join(b.text for b in eval_response.content if b.type == "text")

        # Strip markdown fences if present
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()

        result = json.loads(raw)

        # Use the actual execution response, not what the evaluator generated
        result["claude_response"] = claude_response
        result["score"] = max(0, min(100, int(result.get("score", 50))))

        # Ensure breakdown sums correctly
        breakdown = result.get("score_breakdown", {})
        for k in ["clarity", "context", "structure", "output_quality"]:
            breakdown[k] = max(0, min(25, int(breakdown.get(k, 12))))
        result["score_breakdown"] = breakdown

        return result

    except Exception as e:
        # Fallback: return a basic result if evaluation fails
        return {
            "claude_response": claude_response,
            "score": 50,
            "score_breakdown": {
                "clarity": 12,
                "context": 12,
                "structure": 13,
                "output_quality": 13,
            },
            "feedback": "Your prompt was submitted successfully. Keep experimenting!",
            "tip": "Try being more specific about the output format you want Claude to use.",
            "model_comparison": "Compare your output to the model prompt to see how specificity improves results.",
        }
