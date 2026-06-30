CHALLENGES = [
    # ── JIRA & BACKLOG MANAGEMENT ──────────────────────────────────────────────
    {
        "id": "jira_user_story",
        "category": "jira",
        "category_label": "Jira & Backlog",
        "icon": "🎯",
        "title": "Write a User Story",
        "difficulty": "beginner",
        "xp_reward": 50,
        "scenario": (
            "Your product lead just messaged you: 'We need users to be able to reset their "
            "password — can you write this up as a user story for the sprint?' "
            "Use Claude to transform this rough idea into a fully structured, developer-ready user story."
        ),
        "context": (
            "You're a PM at a fintech startup. Your users frequently get locked out and "
            "the support team spends hours per week on password resets. The dev team uses "
            "standard Agile ceremonies and expects user stories in the format they can act on immediately."
        ),
        "what_makes_a_great_prompt": [
            "Use XML tags to clearly separate different parts of your prompt — wrap your context in <context> tags, your requirements in <requirements> tags, and your output format in <output_format> tags. Claude parses structured prompts significantly more reliably than unstructured prose.",
            "Give Claude a specific role with seniority AND company context: 'You are a senior PM at a Series B fintech startup' outperforms 'You are a PM' because it shapes the vocabulary, risk tolerance, and audience Claude assumes.",
            "List your exact output sections by name rather than describing them vaguely — 'Include: 1) User story in As/Want/So format 2) 6-8 Given/When/Then ACs 3) Out-of-scope list 4) Edge cases' is far more reliable than 'write a complete user story'.",
            "End with a self-check instruction: 'Before finishing, verify that every acceptance criterion is independently testable by a QA engineer who cannot ask follow-up questions.' This catches vague criteria automatically.",
            "Give Claude the business WHY, not just the WHAT — 'Support spends 8+ hours/week on password resets costing $X in labor' gives Claude the context to prioritize edge cases and calibrate the level of detail.",
        ],
        "model_prompt": (
            "You are a senior product manager at a Series B fintech startup.\n\n"
            "<context>\n"
            "Our users frequently get locked out. The support team spends 8+ hours/week on manual "
            "password resets. This user story is for our Agile sprint; engineers will implement "
            "directly from this ticket with no follow-up questions.\n"
            "</context>\n\n"
            "<task>\n"
            "Write a complete, developer-ready user story for a self-service password reset feature.\n"
            "</task>\n\n"
            "<requirements>\n"
            "1. User story in 'As a [user] I want [goal] so that [benefit]' format\n"
            "2. 6-8 acceptance criteria in Given/When/Then format, each independently testable\n"
            "3. Explicit out-of-scope list (minimum 3 items to prevent scope creep)\n"
            "4. Edge cases and error states (expired links, invalid emails, rate limiting)\n"
            "5. Assumptions made (list any decisions taken)\n"
            "</requirements>\n\n"
            "<output_format>\n"
            "Use Jira-compatible markdown. Each AC on its own line prefixed with '- [ ]'.\n"
            "</output_format>\n\n"
            "Before finishing, verify every AC is independently testable and contains no vague words "
            "like 'quickly' or 'easily' — replace any with specific measurable criteria."
        ),
        "evaluation_rubric": (
            "Score this user story submission on 4 dimensions (0-25 each):\n"
            "1. Specificity: Does the output have a proper user story format with clear user/goal/benefit?\n"
            "2. Acceptance Criteria: Are there testable, concrete Given/When/Then criteria?\n"
            "3. Completeness: Does it cover edge cases, error states, and out-of-scope?\n"
            "4. Developer-Ready: Could a developer implement this without asking follow-up questions?"
        ),
    },
    {
        "id": "jira_acceptance_criteria",
        "category": "jira",
        "category_label": "Jira & Backlog",
        "icon": "🎯",
        "title": "Generate Acceptance Criteria",
        "difficulty": "beginner",
        "xp_reward": 50,
        "scenario": (
            "A developer just asked you: 'What does done look like for the new "
            "notification preferences feature?' You have a vague Jira ticket description: "
            "'Users can manage their notification settings.' "
            "Use Claude to turn this into crisp, testable acceptance criteria."
        ),
        "context": (
            "You're working on a SaaS product. The notification preferences feature "
            "lets users control which emails, push notifications, and in-app alerts they receive. "
            "The dev team is blocked and needs this today for sprint planning."
        ),
        "what_makes_a_great_prompt": [
            "Include a worked example using <example> tags to show Claude the exact Given/When/Then format you want — Anthropic's official guidance calls this 'few-shot prompting' and it's one of the highest-leverage prompting techniques. Claude will mirror the format, specificity, and style of your example.",
            "Tell Claude what TO write, not what to avoid — 'Write each criterion as a single, atomic test case' is more effective than 'Don't write vague criteria'. Positive instructions give Claude a clear target; negative instructions just create ambiguity.",
            "Map out all the sub-features explicitly before asking for ACs: 'The feature covers (1) email notification controls, (2) push notification controls, (3) in-app alert controls, (4) save/update behavior, (5) default state on first login' — Claude can only write ACs for things you mention.",
            "Ask Claude to flag ambiguities explicitly: 'If any requirement is ambiguous or would require a design decision, note it with [AMBIGUITY: description]'. This surfaces gaps before dev starts rather than mid-sprint.",
            "Specify a coverage matrix: 'Write at least 2 ACs for each notification type, plus 2 ACs for edge cases' — this prevents Claude from clustering all ACs around the happy path.",
        ],
        "model_prompt": (
            "You are a senior product manager at a B2B SaaS company.\n\n"
            "<context>\n"
            "Feature: Notification Preferences — lets users independently control email notifications, "
            "push notifications, and in-app alerts per category. Dev team needs ACs today for sprint planning.\n"
            "</context>\n\n"
            "<task>\n"
            "Generate 10-12 acceptance criteria for this feature.\n"
            "</task>\n\n"
            "<format_example>\n"
            "Given a logged-in user on the Notification Preferences page\n"
            "When they toggle 'Weekly Digest Email' to OFF and click Save\n"
            "Then the preference is persisted and they receive no weekly digest emails going forward\n"
            "</format_example>\n\n"
            "<requirements>\n"
            "- At least 3 ACs covering email notifications\n"
            "- At least 3 ACs covering push notifications\n"
            "- At least 2 ACs covering in-app alerts\n"
            "- At least 2 ACs for edge cases (unsaved changes, default state, account with no prior prefs)\n"
            "- Flag any ambiguity with [AMBIGUITY: description]\n"
            "</requirements>\n\n"
            "Write each AC in Given/When/Then format. Every AC must be independently testable."
        ),
        "evaluation_rubric": (
            "Score this acceptance criteria submission (0-25 each):\n"
            "1. Coverage: Does it address multiple notification types and scenarios?\n"
            "2. Testability: Are criteria specific enough to write automated tests from?\n"
            "3. Format: Does it use a consistent, structured format (Given/When/Then or similar)?\n"
            "4. Edge Cases: Does it address failure states, defaults, and boundary conditions?"
        ),
    },
    {
        "id": "jira_epic_breakdown",
        "category": "jira",
        "category_label": "Jira & Backlog",
        "icon": "🎯",
        "title": "Break Down an Epic",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "scenario": (
            "You have an epic: 'Build a compliance reporting dashboard for enterprise healthcare customers.' "
            "Four enterprise deals — totaling $2.1M ARR — are blocked in procurement until customers "
            "can run their own audit reports. Sales has committed a Q3 delivery date. "
            "Sprint planning is tomorrow. Use Claude to decompose this epic into a structured backlog."
        ),
        "context": (
            "The dashboard must let hospital compliance officers export HIPAA audit logs, user activity, "
            "and access control reports to PDF/CSV. Your team is 3 engineers in 2-week sprints. "
            "The MVP (audit log export only) is needed in 6 weeks to unblock the deals; "
            "full reporting can follow in subsequent sprints. Non-MVP features must be clearly labeled."
        ),
        "what_makes_a_great_prompt": [
            "Put your constraints in <constraints> tags at the top of your prompt, before the task description — Anthropic research shows that for complex prompts, placing important context before instructions improves output quality because Claude reads it before deciding how to approach the task.",
            "Specify the exact output table columns you want: 'Create a table with columns: Story Title | User-Facing Description (one sentence) | T-shirt Size (S/M/L) | MVP? (yes/no) | Depends On'. Claude formats tables precisely when you name the columns explicitly.",
            "Ask Claude to think through the epic from multiple angles: 'Consider both the frontend stories (what users see) and backend stories (data models, API endpoints) separately, then identify shared infrastructure stories' — this surfaces stories that single-perspective decomposition misses.",
            "Give Claude explicit sequencing rules: 'Label stories as Sprint 1/2/3 based on the rule that backend API stories must precede frontend stories that consume them' — Claude respects logical dependency rules when you state them clearly.",
            "Ask Claude to identify the riskiest assumption in the decomposition: 'After the table, note the one story whose scope is most uncertain and explain why' — this surfaces planning risks before the sprint starts.",
        ],
        "model_prompt": (
            "You are a senior product manager planning a sprint backlog.\n\n"
            "<constraints>\n"
            "- Team: 3 engineers\n"
            "- Sprint length: 2 weeks\n"
            "- MVP deadline: 6 weeks (3 sprints)\n"
            "- Story size cap: no story larger than L (max 5 days one engineer)\n"
            "</constraints>\n\n"
            "<task>\n"
            "Decompose the epic 'Customer-Facing Reporting Dashboard' (revenue metrics, user activity, "
            "PDF/CSV export) into sprint-sized user stories for the backlog.\n"
            "</task>\n\n"
            "<requirements>\n"
            "1. Consider frontend stories, backend/API stories, and shared infrastructure separately\n"
            "2. Output a table: Story Title | One-Line Description | Size (S/M/L) | MVP (yes/no) | Sprint (1/2/3/future) | Depends On\n"
            "3. Group by theme (e.g., Data Layer, Charts, Export, Permissions)\n"
            "4. After the table, identify the single riskiest story with a brief explanation\n"
            "</requirements>\n\n"
            "Sequence stories so no story appears in a sprint before its dependencies."
        ),
        "evaluation_rubric": (
            "Score this epic decomposition (0-25 each):\n"
            "1. Completeness: Are all major components of the epic represented as stories?\n"
            "2. Sizing: Are stories appropriately sized for a sprint (not too large, not too granular)?\n"
            "3. MVP Clarity: Is there a clear separation between MVP and future features?\n"
            "4. Dependencies: Are inter-story dependencies identified and sequenced logically?"
        ),
    },
    {
        "id": "jira_backlog_refinement",
        "category": "jira",
        "category_label": "Jira & Backlog",
        "icon": "🎯",
        "title": "Backlog Refinement Analysis",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "scenario": (
            "You're inheriting an 87-ticket backlog from a PM who left last week. "
            "Q3 planning kicks off in 48 hours and the CEO is already asking what's on the roadmap. "
            "Many tickets are stale, vague, or duplicated — and you've never seen most of them. "
            "Use Claude to rapidly triage, prioritize, and clean up the backlog before planning starts."
        ),
        "context": (
            "Your product is a B2B HR platform. Company OKRs this quarter: increase enterprise "
            "customer retention, reduce time-to-value for new customers, and expand into the "
            "Canadian market. The top 10 items in your backlog are a mix of bugs, features, and tech debt."
        ),
        "what_makes_a_great_prompt": [
            "Give Claude the OKRs in <okrs> tags before describing the task — when Claude knows the strategic goals first, it applies them consistently throughout the analysis rather than retrofitting them to an already-formed opinion.",
            "Name the prioritization framework explicitly (RICE, MoSCoW, value/effort matrix) and define the scoring criteria: 'Score Reach on a 1-10 scale where 10 = affects all enterprise customers' — ambiguous framework definitions produce inconsistent scoring.",
            "Ask Claude to generate a realistic sample backlog rather than working with abstract categories — 'Create 10 realistic backlog items including 4 features, 3 bugs, 2 tech debt items, 1 compliance task' gives Claude concrete material to prioritize, producing more useful output.",
            "Ask for explicit reasoning per item: 'For each item, write one sentence explaining how it maps (or doesn't map) to the OKRs' — this makes the prioritization defensible to stakeholders and surfaces misaligned items clearly.",
            "Request an 'archive' recommendation: 'Flag 3 items that should be closed/archived with justification' — a good backlog refinement explicitly removes items, not just reorders them.",
        ],
        "model_prompt": (
            "You are a senior product manager at a B2B HR platform.\n\n"
            "<okrs>\n"
            "1. Increase enterprise customer retention (NRR target: 115%)\n"
            "2. Reduce time-to-value for new customers (onboarding completion <7 days)\n"
            "3. Expand into Canadian market (localization + compliance)\n"
            "</okrs>\n\n"
            "<task>\n"
            "Using the RICE framework (Reach × Impact × Confidence ÷ Effort), prioritize a sample backlog.\n"
            "</task>\n\n"
            "<requirements>\n"
            "1. Generate 10 realistic backlog items: 4 features, 3 bugs, 2 tech debt items, 1 compliance task\n"
            "2. Score each with RICE (1-10 per dimension, Effort in person-weeks)\n"
            "3. Output a ranked table: Rank | Item | Type | R | I | C | E | RICE Score | OKR Alignment\n"
            "4. Write one sentence per item explaining OKR alignment (or flag as 'no OKR alignment')\n"
            "5. Recommend 3 items to archive with justification\n"
            "</requirements>\n\n"
            "After the table, write a 2-sentence executive summary suitable for the CEO."
        ),
        "evaluation_rubric": (
            "Score this backlog refinement prompt/output (0-25 each):\n"
            "1. Framework: Is a clear prioritization framework applied consistently with defined scoring criteria?\n"
            "2. Strategic Alignment: Are items explicitly scored against the company OKRs, with items flagged that have no OKR alignment?\n"
            "3. Backlog Health: Does the output identify stale, duplicate, or low-value tickets for closure — and propose triage rules for future grooming?\n"
            "4. Actionability: Is the output ready to present to the CEO with a defensible executive summary?"
        ),
    },

    # ── CONFLUENCE & DOCUMENTATION ─────────────────────────────────────────────
    {
        "id": "confluence_meeting_notes",
        "category": "confluence",
        "category_label": "Confluence & Docs",
        "icon": "📄",
        "title": "Structure Meeting Notes",
        "difficulty": "beginner",
        "xp_reward": 50,
        "scenario": (
            "You just got out of a 45-minute product strategy meeting. "
            "You have messy notes but need to publish structured meeting minutes to Confluence "
            "before the end of day. Use Claude to transform your raw notes into professional docs."
        ),
        "context": (
            "The meeting covered: Q3 roadmap priorities, a debate about building vs. buying "
            "an analytics solution, a decision to delay the mobile app launch by 3 weeks, "
            "and action items assigned to 4 team members. Your audience is the broader product org."
        ),
        "what_makes_a_great_prompt": [
            "Name every output section explicitly in a numbered list — 'The document must contain these exact sections: 1) Date & Attendees 2) Executive Summary 3) Decisions (separate from Discussion) 4) Action Items table 5) Open Questions' — Claude faithfully produces named sections when you enumerate them.",
            "Distinguish between decisions and discussion explicitly in your prompt: 'A Decision is a conclusion the group reached with no intent to revisit. Discussion is context and deliberation leading to it. Keep these strictly separated.' Claude conflates them when not instructed otherwise.",
            "Tell Claude the audience and their reading constraint: 'The audience is a 50-person product org. Most will spend 90 seconds scanning, not reading. Write the Executive Summary in 3 sentences max so it can be read in a Slack preview.'",
            "Specify the action item format as a table with specific columns: 'Action Items must be a table with columns: Owner | Action (verb-first) | Due Date | Priority (High/Med/Low)'. Verb-first phrasing ('Schedule demo', not 'Demo needs to be scheduled') makes items immediately actionable.",
            "Give Claude the raw notes as input — even messy shorthand is better than describing the meeting. Wrap them in <raw_notes> tags so Claude knows where instructions end and source material begins.",
        ],
        "model_prompt": (
            "You are a technical writer producing Confluence meeting minutes.\n\n"
            "<raw_notes>\n"
            "Q3 roadmap - agreed to cut features F4 and F5, focus on core retention. Sarah to update roadmap doc by Friday.\n"
            "Build vs buy analytics - Jake argued for Mixpanel ($3K/mo), Lisa said build it, takes 6 weeks. Decided: buy Mixpanel, Jake to start trial Monday.\n"
            "Mobile launch delay - iOS issues with biometric auth on older devices. 3 week delay. Launch now Oct 15. Marketing needs to know.\n"
            "Action items: Jake - Mixpanel trial by Mon. Sarah - update roadmap Fri. Tom - notify marketing re delay today. Lisa - fix biometric bug, estimate by Wed.\n"
            "Attendees: Jake, Sarah, Lisa, Tom, Priya (facilitator)\n"
            "</raw_notes>\n\n"
            "<output_format>\n"
            "Produce a Confluence-ready page with these exact sections:\n"
            "1. Meeting Details (date, attendees, facilitator)\n"
            "2. Executive Summary (3 sentences max — scannable in a Slack preview)\n"
            "3. Decisions (bullet list — each decision starts with the conclusion, rationale in parentheses)\n"
            "4. Discussion Context (brief narrative of key debates — separate from Decisions)\n"
            "5. Action Items (table: Owner | Action — verb-first | Due Date | Priority)\n"
            "6. Open Questions (numbered list of unresolved items)\n"
            "</output_format>\n\n"
            "Use today's date. Write in a professional but direct tone — this will be read by a 50-person org."
        ),
        "evaluation_rubric": (
            "Score this meeting notes prompt/output (0-25 each):\n"
            "1. Structure: Is the output organized with clear, navigable sections?\n"
            "2. Decision Clarity: Are decisions clearly separated from discussion and rationale included?\n"
            "3. Action Items: Are action items complete with owner, action, and due date?\n"
            "4. Professional Quality: Would this be appropriate to publish to a broad team audience?"
        ),
    },
    {
        "id": "confluence_tech_spec",
        "category": "confluence",
        "category_label": "Confluence & Docs",
        "icon": "📄",
        "title": "Write a Technical Spec",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "scenario": (
            "Engineering needs a technical specification before they can start building the "
            "new 'Smart Search' feature. You have high-level requirements but need to "
            "produce a full tech spec doc. Use Claude to draft it."
        ),
        "context": (
            "Smart Search will let users search across all content types (tickets, docs, contacts) "
            "using natural language. It needs to return results in <500ms, support filters, "
            "and rank results by relevance and recency. The system integrates with Elasticsearch."
        ),
        "what_makes_a_great_prompt": [
            "Use XML tags to give Claude a structured template to fill in — '<sections>Problem Statement, Goals, Non-Goals, Functional Requirements, Non-Functional Requirements, API Design, Out of Scope, Open Questions, Dependencies</sections>' works better than prose describing what you want.",
            "Make non-functional requirements measurable by including the numbers in your prompt: '<performance>Response time: <500ms at p95. Concurrent users: 5,000. Query throughput: 100 searches/second peak.</performance>' — Claude treats these as constraints, not suggestions.",
            "Explicitly ask Claude to flag design decisions that need a human to make: 'If a section requires an architectural decision you cannot make from the given information, write [OPEN DECISION: description] instead of guessing.' This surfaces ambiguities rather than hiding them behind confident-sounding prose.",
            "Specify the primary audience and their goal with the spec: 'This spec will be used by 3 backend engineers to implement the feature without further PM involvement. Assume they know Elasticsearch but not our product domain.' This calibrates the level of assumed knowledge.",
            "Ask Claude to add an 'Out of Scope' section with at least 5 items — this is often the most valuable section because it prevents the feature from expanding as engineers encounter adjacent problems during implementation.",
        ],
        "model_prompt": (
            "You are a senior product manager writing a technical specification for an engineering team.\n\n"
            "<context>\n"
            "Feature: Smart Search — natural language search across tickets, docs, and contacts using "
            "Elasticsearch. Primary consumers: 3 backend engineers who will implement without further PM involvement.\n"
            "</context>\n\n"
            "<performance_constraints>\n"
            "- Response time: <500ms at p95\n"
            "- Concurrent users: 5,000\n"
            "- Index freshness: results reflect changes within 60 seconds\n"
            "- Ranking: relevance score × recency decay\n"
            "</performance_constraints>\n\n"
            "<sections_required>\n"
            "1. Problem Statement (why this exists, what pain it solves)\n"
            "2. Goals (measurable success criteria)\n"
            "3. Non-Goals (minimum 5 explicit out-of-scope items)\n"
            "4. Functional Requirements (user-facing behaviors)\n"
            "5. Non-Functional Requirements (performance, security, scalability — each with measurable threshold)\n"
            "6. API Design (endpoint, request/response schema with sample JSON)\n"
            "7. Open Questions (use [OPEN DECISION: description] for architectural decisions requiring input)\n"
            "8. Dependencies and Risks\n"
            "</sections_required>\n\n"
            "Format for Confluence. Write at engineer-level detail — skip PM-level background."
        ),
        "evaluation_rubric": (
            "Score this tech spec prompt/output (0-25 each):\n"
            "1. Completeness: Does it cover all major spec sections (requirements, API, NFRs, risks)?\n"
            "2. Technical Depth: Are requirements specific enough for an engineer to implement from?\n"
            "3. NFRs: Are non-functional requirements (performance, security, scale) addressed?\n"
            "4. Clarity: Is the out-of-scope section clear? Are open questions surfaced?"
        ),
    },
    {
        "id": "confluence_status_report",
        "category": "confluence",
        "category_label": "Confluence & Docs",
        "icon": "📄",
        "title": "Write a Project Status Report",
        "difficulty": "beginner",
        "xp_reward": 50,
        "scenario": (
            "It's Friday and your VP of Product expects a weekly project status report "
            "in Confluence by 5pm. The project is your Q3 platform migration. "
            "Use Claude to produce a polished, executive-ready status update."
        ),
        "context": (
            "Week 6 of 12. You're on track for Phase 1 (data migration — 90% done). "
            "Phase 2 (API migration) is 2 days behind due to a third-party API breaking change. "
            "Risk: if the vendor doesn't respond by Monday, you'll need to escalate. "
            "Budget: on track. Team morale is good."
        ),
        "what_makes_a_great_prompt": [
            "Frame the audience constraint before giving the content: 'This will be read by a VP who has 3 minutes. Lead with overall status, put supporting detail after.' Anthropic research shows audience framing at the start of the prompt — before the data — meaningfully shapes how Claude prioritizes and structures information.",
            "Use RAG (Red/Amber/Green) status explicitly and tell Claude what each color means in your org: 'GREEN = on track, AMBER = at risk but recoverable without executive action, RED = requires executive decision now.' Defining the thresholds produces consistent, defensible ratings.",
            "Include all the numbers directly in your prompt: 'Phase 1: 90% complete. Phase 2: 2 days behind schedule. Budget: $0 variance. Vendor response deadline: Monday.' Claude uses these verbatim — don't describe the situation in narrative when you have precise data.",
            "Tell Claude to write the risk in the RAID format (Risk | Impact | Probability | Mitigation | Owner): 'Present each risk as one row in a RAID table, not as a narrative paragraph.' Tables are faster for executives to scan than prose.",
            "Ask for the 'Decisions Needed' section explicitly and require it to use yes/no questions: 'List any decisions the VP needs to make this week as yes/no questions with the deadline.' Vague asks ('we may need guidance on X') don't produce executive action; specific binary questions do.",
        ],
        "model_prompt": (
            "You are a senior product manager writing a weekly status report for a VP of Product.\n\n"
            "<audience>\n"
            "VP of Product. Reading time: 3 minutes max. Expects: overall status at a glance, "
            "risks with mitigations, and any decisions they need to make. Does not want narrative — wants signal.\n"
            "</audience>\n\n"
            "<project_data>\n"
            "Project: Q3 Platform Migration | Week 6 of 12\n"
            "Phase 1 (Data Migration): 90% complete — GREEN\n"
            "Phase 2 (API Migration): 2 days behind — AMBER (cause: third-party breaking change discovered Mon)\n"
            "Budget: on track, $0 variance\n"
            "Team: morale good, no attrition\n"
            "Risk: Vendor must respond by Monday EOD or Phase 2 slips further; escalation path exists\n"
            "</project_data>\n\n"
            "<output_format>\n"
            "1. Overall Status: one sentence + traffic light (GREEN/AMBER/RED)\n"
            "2. Phase Status Table: Phase | Status | % Complete | Δ vs Plan | Note\n"
            "3. This Week's Progress: 3-5 bullet points, verb-first\n"
            "4. Risks: RAID table — Risk | Impact | Probability | Mitigation | Owner\n"
            "5. Next Week Plan: 3-5 bullet points\n"
            "6. Decisions Needed: yes/no questions with deadline (leave blank if none)\n"
            "</output_format>\n\n"
            "Use plain text tables compatible with Confluence wiki markup."
        ),
        "evaluation_rubric": (
            "Score this status report prompt/output (0-25 each):\n"
            "1. Executive Clarity: Is the overall status immediately clear in the first section?\n"
            "2. RAG Usage: Are Red/Amber/Green statuses used appropriately with context?\n"
            "3. Risk Quality: Are risks stated with specific impact and mitigation plans?\n"
            "4. Brevity: Is it concise enough for a busy VP while still being complete?"
        ),
    },
    {
        "id": "confluence_decision_log",
        "category": "confluence",
        "category_label": "Confluence & Docs",
        "icon": "📄",
        "title": "Document an Architecture Decision",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "scenario": (
            "Your team just made an important architectural decision: to use event-driven "
            "architecture (Kafka) instead of a REST-based polling approach for your data pipeline. "
            "Future developers need to understand WHY. Use Claude to create an ADR (Architecture Decision Record)."
        ),
        "context": (
            "The debate was between REST polling (simpler but high latency, high DB load) vs. "
            "Kafka event streaming (higher ops complexity but real-time, scalable). "
            "Decision made by: CTO + lead engineers. Date: today. "
            "The main drivers: 10x data volume growth expected in 18 months, "
            "SLA requirement of <2s end-to-end latency."
        ),
        "what_makes_a_great_prompt": [
            "Give Claude the standard ADR template structure in <template> tags so it fills in the format exactly — 'Template: Title | Status | Context | Decision | Consequences (positive + negative) | Rejected Alternatives | Future Considerations'. ADRs have a defined format for a reason; specifying it prevents Claude from inventing its own structure.",
            "Tell Claude to be honest about the downsides of the chosen approach — this is the part humans most often omit and it's the most valuable for future developers: 'List at least 3 genuine disadvantages of Kafka vs REST polling. Do not soften or minimize them — future devs need to know what we traded away.'",
            "Ask Claude to write the 'Rejected Alternatives' section with specific scoring: 'For each rejected option, explain what would have to change for it to be the better choice. This frames the decision as conditional rather than absolute, which is more intellectually honest.'",
            "Give Claude both options' concrete tradeoffs in your prompt: REST polling (pros: simple ops, easy debugging; cons: 200ms polling lag, DB hammering at scale) vs Kafka (pros: real-time, scalable; cons: ops complexity, learning curve, new infrastructure). Claude produces more accurate ADRs when the tradeoffs are explicit rather than inferred.",
            "Include the time dimension: 'Note any time pressure or context that affected this decision — a decision made under time pressure or resource constraints is different from a pure technical best-practices choice, and future readers need to know that.'",
        ],
        "model_prompt": (
            "You are a principal engineer writing an Architecture Decision Record for the team knowledge base.\n\n"
            "<decision_context>\n"
            "Decision: Adopt Apache Kafka for our data pipeline instead of REST polling\n"
            "Decided by: CTO + lead engineers\n"
            "Key drivers: 10x data volume growth in 18 months; <2s end-to-end latency SLA\n"
            "REST polling tradeoffs: simpler ops, easy debugging, familiar — but 200ms polling lag, "
            "high DB read load at scale, no fan-out support\n"
            "Kafka tradeoffs: real-time, horizontally scalable, supports fan-out — but ops complexity, "
            "steep learning curve, requires new infrastructure investment\n"
            "</decision_context>\n\n"
            "<template>\n"
            "Title: ADR-[number]: [decision title]\n"
            "Status: Accepted\n"
            "Context: [why this decision needed to be made, constraints and forces]\n"
            "Decision: [what we decided and why in 2-3 sentences]\n"
            "Consequences — Positive: [at least 3 benefits]\n"
            "Consequences — Negative: [at least 3 genuine costs/risks — do not minimize]\n"
            "Rejected Alternatives: [each with: what it is, why rejected, what would need to change to reconsider]\n"
            "Future Considerations: [what this decision forecloses; what could trigger revisiting]\n"
            "</template>\n\n"
            "Write this for a developer who will read it in 2 years and needs to understand "
            "the full context, including what we traded away. Be intellectually honest about the tradeoffs."
        ),
        "evaluation_rubric": (
            "Score this ADR prompt/output (0-25 each):\n"
            "1. ADR Format: Does it follow proper ADR structure (context, decision, consequences)?\n"
            "2. Decision Reasoning: Is the WHY clearly documented with specific drivers?\n"
            "3. Tradeoff Honesty: Are cons of the chosen option acknowledged? Are alternatives explained?\n"
            "4. Future Value: Would a new engineer 2 years from now understand the full context?"
        ),
    },

    # ── STAKEHOLDER COMMUNICATION ──────────────────────────────────────────────
    {
        "id": "stakeholder_delay_email",
        "category": "stakeholder",
        "category_label": "Stakeholder Comms",
        "icon": "📧",
        "title": "Communicate a Project Delay",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "scenario": (
            "Your Q3 flagship feature will be 3 weeks late. This affects the marketing "
            "launch campaign that's already been scheduled. You need to tell your VP of "
            "Marketing and 3 other executives — and they won't be happy. "
            "Use Claude to draft a professional, confidence-inspiring email."
        ),
        "context": (
            "Root cause: an undiscovered third-party API rate limit that required architecture changes. "
            "New date: October 15 (was September 24). "
            "Marketing impact: webinar must be rescheduled, paid ad campaign needs to pause. "
            "You have a mitigation: partial release of core functionality on Oct 1. "
            "Tone needed: accountable, not defensive, solution-focused."
        ),
        "what_makes_a_great_prompt": [
            "Specify the word limit and explain why it matters: 'The email must be under 250 words. Executives receiving bad news need to absorb it quickly — a long email signals defensiveness and buries the plan.' Word constraints force Claude to prioritize signal over noise.",
            "Tell Claude the structure you want as an ordered sequence: 'Structure: (1) What happened and new date — first sentence (2) What we're doing about it — paragraph 2 (3) Impact on marketing and mitigation — paragraph 3 (4) Next steps — final bullet list.' This is more reliable than letting Claude infer structure from a vague description.",
            "Give Claude explicit tone guidance with a contrast: 'Tone: accountable and solution-focused. NOT: defensive (no long technical explanation), NOT: apologetic-to-the-point-of-groveling (confidence is required), NOT: optimistic spin (executives need to trust you're being straight).'",
            "Tell Claude what NOT to put in the subject line by contrasting good and bad examples: 'Subject line should name the delay directly, e.g. \"Feature X Launch Update — New Date Oct 15\". Avoid vague subjects like \"Important Update\" that force re-reads to understand the urgency.'",
            "Ask Claude to write two versions — one for the VP of Marketing (most impacted) and a shorter BCC version for the other executives: 'The VP Marketing version should include the specific impact on the webinar and ad campaign. The exec version can be 3 sentences.'",
        ],
        "model_prompt": (
            "You are a VP of Product writing a delay notification email.\n\n"
            "<audience>\n"
            "Primary: VP Marketing (most impacted — her webinar and ad campaign must move)\n"
            "BCC: CEO, CFO, Head of Sales\n"
            "</audience>\n\n"
            "<facts>\n"
            "- Feature delayed: Q3 flagship feature\n"
            "- Original launch: September 24\n"
            "- New launch: October 15 (3 weeks)\n"
            "- Root cause: third-party API rate limit discovered during load testing requiring architecture change\n"
            "- Marketing impact: webinar must reschedule; paid ad campaign pauses ~2 weeks\n"
            "- Mitigation: partial release of core functionality October 1 (reduces gap)\n"
            "</facts>\n\n"
            "<format>\n"
            "Write two versions:\n"
            "VERSION 1 — VP Marketing (under 250 words):\n"
            "Structure: (1) New date, upfront (2) Root cause, one sentence (3) Marketing impact + mitigation (4) Next steps as bullet list\n"
            "Tone: accountable, solution-focused, confident — not defensive or apologetic\n\n"
            "VERSION 2 — Executive BCC (under 75 words):\n"
            "Just the key facts: what, new date, mitigation, and one ask if needed\n"
            "</format>\n\n"
            "Include subject lines for both. Name the delay in the subject line directly."
        ),
        "evaluation_rubric": (
            "Score this delay communication prompt/output (0-25 each):\n"
            "1. Accountability: Is the delay owned clearly without being defensive or over-explaining?\n"
            "2. Solution Focus: Is the mitigation plan front and center, not buried?\n"
            "3. Audience Calibration: Is it written for executives (business impact, not technical details)?\n"
            "4. Conciseness: Is it under 300 words while still complete?"
        ),
    },
    {
        "id": "stakeholder_risk_escalation",
        "category": "stakeholder",
        "category_label": "Stakeholder Comms",
        "icon": "📧",
        "title": "Escalate a Project Risk",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "scenario": (
            "A critical vendor just announced they're sunsetting the API your product depends on "
            "in 90 days. This is a HIGH severity risk. You need to escalate this to the "
            "executive team immediately and get a decision on how to respond. "
            "Use Claude to draft the escalation communication."
        ),
        "context": (
            "The API provides your payment processing integration. Migrating to a new vendor "
            "takes ~3 months of engineering work. Options: 1) Start migration now (costs $150K), "
            "2) Request API extension from vendor (uncertain), 3) Use interim wrapper (2-week dev, buys time). "
            "You need a go/no-go decision within 48 hours to stay on schedule."
        ),
        "what_makes_a_great_prompt": [
            "Frame the communication as a decision request, not an FYI — tell Claude this explicitly: 'This is a decision request, not an informational update. Every section should move toward the decision. End with a single binary question and a deadline.' Without this instruction, Claude defaults to informational framing.",
            "Ask for a structured options table with specific columns: 'Present options in a table: Option | Engineering Time | Cost | Risk Level | Recommendation (yes/no)'. A table forces apples-to-apples comparison and is the format executives make decisions from fastest.",
            "Include the urgency driver in the prompt: 'The 48-hour deadline exists because starting the migration 2 days late cascades into a 2-week project slip due to sprint allocation cycles — include this causal chain in the escalation so executives understand why speed matters.'",
            "Tell Claude to write the recommended path as a clear recommendation with rationale, not a hedge: 'State a single recommended option with 2-3 bullet points of reasoning. Do not write \"we recommend option 2 but option 3 is also viable\" — pick one and defend it.'",
            "Specify the reading context: 'This will be read on mobile during a meeting. Use short paragraphs, bold the option names, and put the decision question in its own box at the end.' Claude adapts formatting to reading context when you describe it.",
        ],
        "model_prompt": (
            "You are a senior product manager writing a risk escalation to the executive team.\n\n"
            "<context>\n"
            "Payment processing API vendor sunsetting in 90 days. Three options available. "
            "Need a go/no-go decision within 48 hours — delay cascades into a 2-week project slip "
            "due to sprint allocation cycles. This is a decision request, not an informational update.\n"
            "</context>\n\n"
            "<options>\n"
            "1. Full migration now: 3 months engineering, $150K cost, eliminates dependency permanently\n"
            "2. Vendor extension request: 0 cost, uncertain outcome, buys 3-6 months if granted\n"
            "3. Interim wrapper: 2 weeks, $20K, buys time while deciding on long-term path\n"
            "</options>\n\n"
            "<output_format>\n"
            "1. Risk Summary (2 sentences: what + business impact if unaddressed)\n"
            "2. Options Table: Option | Time | Cost | Risk Level | Viable? (yes/no)\n"
            "3. Recommended Path (name it, give 3 bullet-point rationale — no hedging)\n"
            "4. Decision Box: [bold, visually separated] — single yes/no question + deadline\n"
            "</output_format>\n\n"
            "Under 400 words total. Readable on mobile in 2 minutes."
        ),
        "evaluation_rubric": (
            "Score this risk escalation prompt/output (0-25 each):\n"
            "1. Urgency: Is the severity and timeline communicated clearly upfront?\n"
            "2. Options Clarity: Are 3+ options presented with tradeoffs in a scannable format?\n"
            "3. Decision Request: Is there a specific, binary decision request with a clear deadline?\n"
            "4. Executive Calibration: Is business impact (cost, risk, time) leading over technical detail?"
        ),
    },
    {
        "id": "stakeholder_quarterly_update",
        "category": "stakeholder",
        "category_label": "Stakeholder Comms",
        "icon": "📧",
        "title": "Quarterly Product Update",
        "difficulty": "beginner",
        "xp_reward": 50,
        "scenario": (
            "It's end of Q2 and you've just been promoted to VP of Product — this is your first "
            "board update. The board was skeptical of the previous roadmap and you need to establish "
            "credibility fast. Your CEO wants a one-page product update by tomorrow morning. "
            "Use Claude to create a polished, board-ready quarterly update that earns their trust."
        ),
        "context": (
            "Q2 highlights: shipped 3 major features (SSO, API v2, Advanced Reporting), "
            "grew MAU by 23%, reduced churn from 4.2% to 3.1%, launched in Canada. "
            "Q3 priorities: Mobile app launch, AI-powered search, SOC2 compliance. "
            "One challenge: engineering headcount is 2 below plan."
        ),
        "what_makes_a_great_prompt": [
            "Lead with outcomes, not outputs — tell Claude explicitly: 'Frame wins as business outcomes, NOT feature deliveries. NOT: \"We shipped SSO, API v2, and Advanced Reporting.\" YES: \"NRR grew to 112% and churn dropped to 3.1% — driven by SSO unblocking 6 enterprise deals and Advanced Reporting reducing support tickets 28%.\" Boards fund outcomes, not feature counts.'",
            "Tell Claude the board's primary concerns explicitly: 'This board cares about: revenue health (NRR, churn), product-market fit signals (MAU growth), and strategic execution. Frame every bullet through one of these three lenses — if a point doesn't connect to one of these, cut it.' Without this filter, Claude writes for a general audience, not an investor audience.",
            "Use <wins> and <challenges> XML tags to feed Claude both sides: 'Include one honest challenge (engineering headcount 2 below plan) with a concrete mitigation — boards distrust updates with no challenges, and a new VP with no challenges looks naive. NOT: vague acknowledgment. YES: specific problem + specific plan to fix it.'",
            "Specify the format as a one-pager with scanning hierarchy: 'Output a one-pager. ## headers, bold the key numbers, bullet points for wins and priorities. NO narrative paragraphs — board members spend 90 seconds on this document. Every sentence must survive the scan test: does it land in 3 seconds?'",
            "Ask Claude to write a 'Key Learning' sentence: 'After the wins section, add one sentence starting with \"Key learning:\" — something non-obvious the team discovered this quarter. This is the highest-credibility signal in the document; it tells the board you reflect, not just execute.'",
        ],
        "model_prompt": (
            "You are a VP of Product preparing a quarterly update for the board of directors.\n\n"
            "<q2_metrics>\n"
            "MAU: +23% QoQ | Churn: 4.2% → 3.1% | Shipped: SSO, API v2, Advanced Reporting | "
            "Launched: Canada | NRR: 112% (up from 108% in Q1)\n"
            "</q2_metrics>\n\n"
            "<q2_challenges>\n"
            "Engineering headcount 2 below plan (2 open reqs, hiring in progress)\n"
            "</q2_challenges>\n\n"
            "<q3_priorities>\n"
            "1. Mobile app launch (iOS + Android) — target Q3 end\n"
            "2. AI-powered search — differentiator for enterprise expansion\n"
            "3. SOC2 compliance — blocker for 4 enterprise deals in pipeline\n"
            "</q3_priorities>\n\n"
            "<board_context>\n"
            "Board cares about: revenue health (NRR, churn), product-market fit (MAU, engagement), "
            "strategic execution. Frame everything through one of these three lenses.\n"
            "</board_context>\n\n"
            "<output_format>\n"
            "One-pager. Use ## headers, bold key numbers, bullet points for wins/priorities.\n"
            "Sections: Q2 Headline Metrics (visual, 4-5 numbers) | Key Wins (3-5 bullets with business impact) | "
            "Key Learning (one sentence) | Challenge + Mitigation | Q3 Priorities (3 bullets, with why each matters to the board)\n"
            "</output_format>"
        ),
        "evaluation_rubric": (
            "Score this quarterly update prompt/output (0-25 each):\n"
            "1. Outcome Framing: Are wins expressed as business outcomes (NRR, churn, revenue impact) rather than features shipped?\n"
            "2. Board Relevance: Is everything framed through investor-relevant lenses (revenue health, product-market fit, strategic execution) — or does it read like a PM status report?\n"
            "3. Completeness: Does it cover wins, one honest challenge with mitigation, and forward-looking priorities with strategic rationale?\n"
            "4. Scannability: Could a board member extract the full picture in 90 seconds — bold numbers, bullet points, no narrative paragraphs?"
        ),
    },
    {
        "id": "stakeholder_alignment_doc",
        "category": "stakeholder",
        "category_label": "Stakeholder Comms",
        "icon": "📧",
        "title": "Stakeholder Alignment Document",
        "difficulty": "beginner",
        "xp_reward": 50,
        "scenario": (
            "Sales, Marketing, and Engineering all have conflicting expectations about the "
            "new CRM integration feature. You need to get everyone aligned BEFORE development "
            "starts. Use Claude to create a stakeholder alignment document."
        ),
        "context": (
            "Sales wants Salesforce integration in 4 weeks. "
            "Marketing wants HubSpot integration and wants to be able to see customer data. "
            "Engineering says any integration is 8 weeks minimum. "
            "You need to document the agreed scope, timeline, and non-scope before kick-off."
        ),
        "what_makes_a_great_prompt": [
            "Feed Claude each stakeholder's stated position in <stakeholder> tags so the tension is explicit: '<stakeholder role=\"Sales\">Wants Salesforce, needs it in 4 weeks</stakeholder> <stakeholder role=\"Engineering\">Says any integration is 8 weeks minimum</stakeholder>'. Claude resolves conflicts more effectively when it has each party's position clearly separated.",
            "Ask Claude to make the scope decision explicit with a rationale, not just a list: 'Capture the scope as two sections: \"Included in this release (with rationale)\" and \"Explicitly excluded (with rationale)\". Each item in the excluded list should reference which stakeholder request it addresses and why it was descoped.'",
            "Tell Claude to format open questions as a table with owners and dates: 'Open Questions must be a table: # | Question | Owner | Due Date | Blocking? (yes/no)'. Unowned open questions never get resolved — the table format forces accountability.",
            "Ask Claude to write a conflict resolution summary: 'Include a section called \"How We Resolved the Disagreement\" that explains the tradeoff made (e.g., we chose Salesforce over HubSpot because Sales drives more revenue). This is the most important section for preventing the debate from re-opening next sprint.'",
            "Specify that the document needs a sign-off section: 'End with a Sign-Off section with blank lines for each stakeholder's name and date. The existence of a sign-off section changes stakeholder behavior — they read the document more carefully before signing.'",
        ],
        "model_prompt": (
            "You are a senior product manager facilitating a stakeholder alignment session.\n\n"
            "<stakeholder_positions>\n"
            "<stakeholder role=\"Sales\">Wants Salesforce CRM integration, needs it in 4 weeks for a deal they're closing</stakeholder>\n"
            "<stakeholder role=\"Marketing\">Wants HubSpot integration + read access to customer data for campaign targeting</stakeholder>\n"
            "<stakeholder role=\"Engineering\">Any CRM integration is minimum 8 weeks; doing both simultaneously is not feasible</stakeholder>\n"
            "</stakeholder_positions>\n\n"
            "<resolution>\n"
            "Agreed approach: Salesforce in Phase 1 (8 weeks, Sales priority), HubSpot in Phase 2 (date TBD). "
            "Marketing data access: read-only view via Salesforce in Phase 1.\n"
            "</resolution>\n\n"
            "<output_format>\n"
            "1. Background (2 sentences: what conflicted and what this doc resolves)\n"
            "2. Included in Phase 1 (bulleted, with rationale per item)\n"
            "3. Explicitly Excluded (bulleted, with which stakeholder request it addresses and why deferred)\n"
            "4. How We Resolved the Disagreement (narrative — 1 paragraph)\n"
            "5. Timeline Agreement (Phase 1 milestones with dates)\n"
            "6. Open Questions (table: # | Question | Owner | Due Date | Blocking?)\n"
            "7. Sign-Off (stakeholder name | role | date — blank for signatures)\n"
            "</output_format>"
        ),
        "evaluation_rubric": (
            "Score this alignment document prompt/output (0-25 each):\n"
            "1. Tension Resolution: Is the conflict between stakeholders explicitly addressed?\n"
            "2. Scope Clarity: Is what's in AND out of scope crystal clear?\n"
            "3. Open Questions: Are unresolved items captured with owners and dates?\n"
            "4. Usability: Would all 3 stakeholders agree this accurately captures the alignment?"
        ),
    },

    # ── DEV TEAM COLLABORATION ─────────────────────────────────────────────────
    {
        "id": "dev_sprint_planning",
        "category": "devteam",
        "category_label": "Dev Team Collab",
        "icon": "💻",
        "title": "Sprint Planning Summary",
        "difficulty": "beginner",
        "xp_reward": 50,
        "scenario": (
            "Sprint planning just ended. You committed to 6 user stories for Sprint 14. "
            "You need to document the sprint goals, capacity decisions, and dependencies "
            "in Confluence so the broader team knows what's happening. "
            "Use Claude to create the sprint planning summary."
        ),
        "context": (
            "Sprint 14 goal: complete user authentication v2 and payment refactor. "
            "Team capacity: 3 engineers at 8 points each = 24 total points. "
            "Committed: 22 points. 2 stories depend on a backend API being ready by day 5. "
            "One engineer will be out on Thursday. Carry-over from Sprint 13: 2 stories."
        ),
        "what_makes_a_great_prompt": [
            "Lead with the sprint goal, not the ticket list — 'The sprint goal is: Complete user auth v2 and payment refactor so that enterprise customers can log in with SSO by end of sprint.' A goal with a \"so that\" explains the why, making the sprint doc useful as a decision-making tool during the sprint, not just a record.",
            "Give Claude the capacity data as numbers, not descriptions: '<capacity>3 engineers × 8 points = 24 points total. Committed: 22 points. 2 points buffer. Engineer A out Thursday (counted as 6-point capacity).</capacity>' Claude uses numbers precisely when they're structured, but infers incorrectly when they're buried in prose.",
            "Ask Claude to format dependencies as a blocker table: 'Dependencies must be a table: Story | Depends On | Who Provides It | Needed By (Day X) | Blocker? (yes/no)'. Engineers reference this table daily — a prose description of dependencies doesn't serve the same purpose.",
            "Ask for a Definition of Done for the sprint goal specifically (not just individual stories): 'At the bottom, write a 3-bullet sprint DoD: what must be true for this sprint goal to be considered met, not just individual stories complete.' Sprint-level DoD prevents the \"all stories closed but goal not met\" situation.",
            "Specify the use case: 'This doc will be referenced during the 10-minute daily standup. Format it so any engineer can quickly find: what they're working on, what's blocking them, and what the overall goal is without reading the whole page.'",
        ],
        "model_prompt": (
            "You are a product manager writing a sprint planning summary for the engineering team.\n\n"
            "<sprint_goal>\n"
            "Sprint 14 goal: Complete user authentication v2 and payment refactor so that "
            "enterprise customers can log in with SSO and process payments by sprint end.\n"
            "</sprint_goal>\n\n"
            "<capacity>\n"
            "Engineers: 3 | Points per engineer: 8 | Total capacity: 24 pts\n"
            "Committed: 22 pts | Buffer: 2 pts\n"
            "Note: Engineer C out Thursday (capacity counted as 6 pts this sprint)\n"
            "Carry-over from Sprint 13: 2 stories (User Invite Flow — 5 pts, Email Templates — 3 pts)\n"
            "</capacity>\n\n"
            "<dependencies>\n"
            "Stories US-45 and US-47 depend on Backend Auth API endpoint being ready by Day 5\n"
            "</dependencies>\n\n"
            "<output_format>\n"
            "1. Sprint Goal (with 'so that' framing)\n"
            "2. Capacity Table: Engineer | Capacity (pts) | Notes\n"
            "3. Committed Stories: Story | Owner | Points | Status\n"
            "4. Carry-Over Context (what it is, why it's here, priority)\n"
            "5. Dependencies Table: Story | Depends On | Provider | Needed By | Blocker?\n"
            "6. Risks (2-3 bullets: what could go wrong and the mitigation)\n"
            "7. Sprint Definition of Done (3 bullets — what must be true for the GOAL to be met)\n"
            "</output_format>\n\n"
            "Format for a Confluence page the team references during 10-minute daily standups."
        ),
        "evaluation_rubric": (
            "Score this sprint planning summary (0-25 each):\n"
            "1. Goal Clarity: Is the sprint goal specific and measurable?\n"
            "2. Capacity Transparency: Are commitment decisions clearly tied to capacity data?\n"
            "3. Risk Visibility: Are dependencies and risks called out proactively?\n"
            "4. Team-Usable: Would an engineer find this useful during a 10-minute standup?"
        ),
    },
    {
        "id": "dev_bug_report",
        "category": "devteam",
        "category_label": "Dev Team Collab",
        "icon": "💻",
        "title": "Write a Clear Bug Report",
        "difficulty": "beginner",
        "xp_reward": 50,
        "scenario": (
            "A customer reported that their payment fails when using a discount code. "
            "You've reproduced it internally. Before handing to engineering, "
            "use Claude to write a thorough, actionable bug report that will get fixed fast."
        ),
        "context": (
            "The bug: When a valid 20% discount code is applied at checkout, the total "
            "updates correctly in the UI but payment processing fails with error code 4011. "
            "Affects: all users with discount codes. Platform: web only (not mobile). "
            "First reported: yesterday. Severity: critical — blocking purchases."
        ),
        "what_makes_a_great_prompt": [
            "Give Claude the error code and ask it to hypothesize root causes: 'Error code 4011 is present. Based on standard payment processing patterns, list 3 likely root causes this engineer should investigate first.' Claude's hypotheses narrow the debugging search space and are usually directionally correct.",
            "Ask for steps to reproduce as a numbered list with environment specifics: 'Steps to reproduce must be a numbered list where each step is a single action. Include: browser (Chrome v124), user account type (free tier with valid discount code), and expected state at each step.' A bug that can be reproduced in one try gets fixed in one day; one that can't gets deprioritized.",
            "Specify the 'Expected vs Actual Behavior' as a two-column format rather than narrative: 'Write Expected and Actual as side-by-side bullets, not prose. Prose buries the delta; the table shows it instantly.' This formatting guidance produces dramatically more scannable bug reports.",
            "Ask for a customer-facing workaround as a separate section: 'Include a Workaround section: what can support tell affected customers to do right now while the bug is being fixed? Even if the answer is there is no workaround, state it explicitly so support doesn't waste time looking.'",
            "Tell Claude the Jira import format you need: 'Format for Jira: use **bold** for section headers, use - for bullets. Include a one-line Summary field (under 60 chars) that will be the ticket title.' Format-aware prompts produce copy-paste-ready output instead of output that needs reformatting.",
        ],
        "model_prompt": (
            "You are a product manager writing a critical priority bug report for the engineering team.\n\n"
            "<bug_facts>\n"
            "Summary: Checkout fails when valid discount code applied\n"
            "Severity: Critical — blocking all purchases with discount codes\n"
            "Error code: 4011 (payment processor rejection)\n"
            "Platform: Web only (not mobile)\n"
            "Scope: All users with valid discount codes\n"
            "Reported: Yesterday by customer; reproduced internally today\n"
            "Behavior: UI total updates correctly (discount applied) but payment processing fails\n"
            "</bug_facts>\n\n"
            "<output_format>\n"
            "**Summary** (under 60 chars — this will be the Jira ticket title)\n"
            "**Severity & Impact** (who is affected, business impact in concrete terms)\n"
            "**Steps to Reproduce** (numbered list, single action per step, with browser + account type)\n"
            "**Expected Behavior** (bullet)\n"
            "**Actual Behavior** (bullet — make the delta with Expected obvious)\n"
            "**Environment** (browser versions, account types, OS confirmed)\n"
            "**Error Details** (code 4011 + any console errors)\n"
            "**Root Cause Hypotheses** (3 likely causes to investigate, based on error 4011 patterns)\n"
            "**Customer Workaround** (what support can tell affected users right now)\n"
            "**Priority** (P0/P1/P2 with justification)\n"
            "</output_format>"
        ),
        "evaluation_rubric": (
            "Score this bug report prompt/output (0-25 each):\n"
            "1. Reproducibility: Are steps to reproduce specific enough to reproduce on first try?\n"
            "2. Technical Completeness: Are error codes, environment, and impact included?\n"
            "3. Severity Assessment: Is the business impact and urgency clearly stated?\n"
            "4. Engineer-Ready: Could a dev start debugging immediately from this report?"
        ),
    },
    {
        "id": "dev_api_requirements",
        "category": "devteam",
        "category_label": "Dev Team Collab",
        "icon": "💻",
        "title": "Define API Requirements",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "scenario": (
            "Your mobile team needs a new API endpoint to power a 'recent activity' feed. "
            "You need to write the API requirements document before the backend team "
            "starts designing. Use Claude to produce a clear, complete API requirements doc."
        ),
        "context": (
            "The activity feed shows: last 50 events per user (logins, purchases, profile updates, etc.). "
            "It needs pagination, filtering by event type, and must respond in <200ms. "
            "The mobile app polls this every 60 seconds. "
            "Auth: existing JWT token. Rate limit needed. PII must be masked."
        ),
        "what_makes_a_great_prompt": [
            "Ask for a sample JSON request and response payload as part of the spec — this is the single most valuable section for backend engineers: 'Include a complete sample JSON response with 3 example events showing all fields, including masked PII fields (e.g., email shown as \"j***@company.com\"). Engineers implement from the payload shape, not from prose descriptions.'",
            "Put the non-functional requirements in <nfr> tags with exact thresholds: '<nfr>Response time: <200ms at p95. Rate limit: 60 requests/minute per user. Payload size limit: 50KB. Mobile polling interval: 60 seconds — design caching accordingly.</nfr>' Vague NFRs like 'fast' and 'lightweight' produce implementations that technically satisfy the spec but fail in production.",
            "Tell Claude to write the error response schema with specific HTTP codes: 'Define error responses for: 401 Unauthorized, 403 Forbidden, 429 Rate Limited, 500 Internal Error. Each error must include: HTTP code, error code string, human-readable message, and retry guidance.' Engineers write error handling from this spec.",
            "Ask Claude to write a 'consumer perspective' section: 'After the technical spec, add a section called \"What the Mobile Team Needs to Know\" — 3-4 bullets written for an iOS engineer, not a backend engineer. Cover: how to authenticate, when to poll vs. use push, and how to handle pagination.' Dual-audience specs prevent integration misunderstandings.",
            "Specify the security requirements explicitly: 'Security requirements must be their own numbered section: (1) PII masking rules per field type (2) JWT validation requirements (3) Rate limiting scope (per user? per IP? both?) (4) Data the API must never expose even if requested.' Security requirements written as prose often get missed; a numbered list gets reviewed.",
        ],
        "model_prompt": (
            "You are a senior product manager writing an API requirements document.\n\n"
            "<context>\n"
            "API: GET /v1/users/{userId}/activity — Recent Activity Feed\n"
            "Consumer: Mobile team (iOS + Android), polling every 60 seconds\n"
            "Backend team will implement from this doc without further PM involvement\n"
            "</context>\n\n"
            "<nfr>\n"
            "Response time: <200ms at p95 | Rate limit: 60 req/min per user\n"
            "Payload: last 50 events | Pagination: cursor-based | PII: masked\n"
            "Auth: existing JWT token | Events: logins, purchases, profile updates, password changes\n"
            "</nfr>\n\n"
            "<output_format>\n"
            "1. Endpoint Overview (method, path, purpose — 2 sentences)\n"
            "2. Request Spec (headers, path params, query params with types and descriptions)\n"
            "3. Response Spec (complete sample JSON with 3 example events, all fields shown, PII masked)\n"
            "4. Pagination Design (cursor-based, explain the cursor format and next-page pattern)\n"
            "5. Error Responses (table: HTTP Code | Error String | Message | Retry Guidance)\n"
            "6. Security Requirements (numbered: PII masking rules | JWT validation | Rate limiting scope | Data never to expose)\n"
            "7. Non-Functional Requirements (measurable thresholds in table form)\n"
            "8. What the Mobile Team Needs to Know (3-4 bullets written for an iOS engineer)\n"
            "</output_format>"
        ),
        "evaluation_rubric": (
            "Score this API requirements prompt/output (0-25 each):\n"
            "1. Completeness: Are all required fields, params, and response formats specified?\n"
            "2. Technical Spec Quality: Is the sample JSON payload realistic and complete?\n"
            "3. Non-Functional Coverage: Are performance, rate limiting, and auth addressed?\n"
            "4. Security: Are PII masking and security requirements explicitly called out?"
        ),
    },
    {
        "id": "dev_technical_handoff",
        "category": "devteam",
        "category_label": "Dev Team Collab",
        "icon": "💻",
        "title": "Technical Handoff Document",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "scenario": (
            "Your lead engineer is going on parental leave in 2 weeks. "
            "They're the only one who fully understands the payment processing module. "
            "You need to create a comprehensive handoff document so the team isn't blocked. "
            "Use Claude to draft the technical handoff doc."
        ),
        "context": (
            "The payment module handles: Stripe integration, subscription billing, "
            "refund processing, webhook handling. Known gotchas: idempotency key handling, "
            "webhook signature verification. There are 3 pending tickets in this area. "
            "The engineer will be available async for 2 weeks post-leave."
        ),
        "what_makes_a_great_prompt": [
            "Tell Claude to write from the perspective of the person inheriting the system cold: 'Write this as if the reader is a competent engineer who is picking up this codebase on Day 1 with no prior context and no access to the original engineer. Every section should answer: what would they need to know to not break something in their first week?'",
            "Make the 'Gotchas and Known Issues' section the most prominent part — tell Claude this explicitly: 'The Gotchas section is the most valuable section of this document. Other sections are discoverable from code; gotchas are not. Write at least 5 specific gotchas. Format each as: Gotcha | What Goes Wrong If You Miss It | How to Handle It Correctly.'",
            "Ask for runbook-style guidance using an if/then format: 'For each common incident type, write a runbook entry in the format: Symptom → Likely Cause → First 3 Things to Check → Resolution Path → Who to Escalate To.' If/then runbooks are faster to use under pressure than narrative explanations.",
            "Ask Claude to format pending work as a prioritized table with context: 'Pending work must be a table: Ticket # | Title | Priority (P0-P3) | Context (why it exists, what decision led to it) | Recommended Approach | Complexity'. The context column is critical — without it, the inheriting engineer treats all tickets as equally mysterious.",
            "Include a contact map: 'Add a \"Who to Ask\" section: if question is about X, contact Y via Z channel. Cover: Stripe integration questions, billing disputes, PCI compliance questions, and infrastructure/deployment.' The handoff fails if the inheriting engineer doesn't know who to call when the runbook doesn't solve it.",
        ],
        "model_prompt": (
            "You are a lead software engineer creating a technical handoff document before parental leave.\n\n"
            "<system_overview>\n"
            "Payment processing module: Stripe integration, subscription billing, refund processing, webhook handling\n"
            "Known gotchas: idempotency key handling (duplicate charges if not handled correctly), "
            "webhook signature verification (silent failures if STRIPE_WEBHOOK_SECRET not set correctly)\n"
            "Pending tickets: 3 open items in this area\n"
            "Availability: async for 2 weeks post-leave (Slack DM only, 24h response time)\n"
            "</system_overview>\n\n"
            "<audience>\n"
            "A competent engineer picking this up on Day 1 with no prior context.\n"
            "Goal: they should not break anything in their first week.\n"
            "</audience>\n\n"
            "<output_format>\n"
            "1. System Overview (architecture in plain English, key files/modules to know)\n"
            "2. Gotchas & Known Issues (table: Gotcha | What Breaks If Missed | How to Handle — minimum 5 items)\n"
            "3. Common Incidents Runbook (format: Symptom → Likely Cause → First 3 Checks → Resolution → Escalate To)\n"
            "4. Pending Work (table: Ticket | Priority | Context | Recommended Approach | Complexity)\n"
            "5. Testing Guide (how to test payment flows safely in staging — what NOT to do)\n"
            "6. Who to Ask (if question is about X → contact Y via Z)\n"
            "7. Reference Links (Stripe docs, internal wikis, monitoring dashboards)\n"
            "</output_format>"
        ),
        "evaluation_rubric": (
            "Score this handoff document prompt/output (0-25 each):\n"
            "1. Cold-Start Value: Would someone new immediately know how to work in this area?\n"
            "2. Gotchas Quality: Are the tricky parts, edge cases, and known issues documented?\n"
            "3. Runbook Presence: Is there actionable guidance for common incidents/tasks?\n"
            "4. Completeness: Are pending work, contacts, and references all captured?"
        ),
    },

    # ── REQUIREMENTS & USE CASES ───────────────────────────────────────────────
    {
        "id": "req_use_case",
        "category": "requirements",
        "category_label": "Requirements",
        "icon": "🔍",
        "title": "Write a Use Case Document",
        "difficulty": "beginner",
        "xp_reward": 50,
        "scenario": (
            "Your team needs a use case document for the new 'Team Analytics' feature "
            "before design starts. Use Claude to create a comprehensive use case doc "
            "that designers, engineers, and QA can all reference."
        ),
        "context": (
            "Team Analytics lets managers view team productivity metrics: "
            "tickets completed, velocity trends, cycle time. "
            "Primary actor: team manager. Secondary actors: individual contributors (read-only), "
            "HR (for compliance exports). Data refreshes daily. "
            "Managers can drill down by time period, team member, or project."
        ),
        "what_makes_a_great_prompt": [
            "Map all actors and their distinct goals in <actors> tags before describing the use cases: '<actors><actor role=\"Manager\" goal=\"Monitor team velocity to plan capacity and identify blockers\"/><actor role=\"IC\" goal=\"View own metrics without seeing peers data\"/><actor role=\"HR\" goal=\"Export compliance reports quarterly\"/></actors>'. Actors with unclear goals produce use cases that conflate multiple user needs.",
            "Ask Claude to write pre-conditions and post-conditions for every use case — these are often skipped but are the most valuable part for QA: 'Pre-condition: what must be true in the system BEFORE this use case begins. Post-condition: what must be true AFTER it completes successfully. Both must be testable system states, not user intentions.'",
            "Explicitly ask for exception flows, not just alternative flows: 'Alternative flow = a different way to succeed. Exception flow = something that prevents success. Write at least one exception flow per use case (e.g., data not available, permission denied, export file too large).' Most use case docs miss exceptions entirely.",
            "Ask Claude to surface a use case the team likely hasn't thought of: 'After writing the requested use cases, identify one non-obvious use case that this feature enables — something the team probably didn't put in the requirements but that users will attempt.' This is a high-value prompt addition that consistently surfaces blind spots.",
            "Tell Claude to label each use case with priority and multi-role impact: 'Label each use case: Priority (Must Have / Should Have / Nice to Have) and Roles Affected (list all actors). This lets the design team immediately see which flows to prototype first and which roles are most impacted.'",
        ],
        "model_prompt": (
            "You are a senior product manager writing a use case document for design and QA.\n\n"
            "<actors>\n"
            "<actor role=\"Manager\" goal=\"Monitor team productivity metrics to plan capacity and surface blockers\"/>\n"
            "<actor role=\"Individual Contributor\" goal=\"View own metrics only — cannot see peer data\"/>\n"
            "<actor role=\"HR\" goal=\"Export quarterly compliance reports with aggregate data\"/>\n"
            "</actors>\n\n"
            "<feature_scope>\n"
            "Team Analytics: view velocity trends, tickets completed, cycle time. "
            "Drill-down by time period, team member, project. Daily data refresh. Compliance export.\n"
            "</feature_scope>\n\n"
            "<use_case_template>\n"
            "Use Case Name | ID: UC-[n]\n"
            "Primary Actor | Goal\n"
            "Pre-conditions (testable system state before)\n"
            "Main Flow (numbered steps)\n"
            "Alternative Flows (different path to success)\n"
            "Exception Flows (what prevents success — minimum 1 per UC)\n"
            "Post-conditions (testable system state after success)\n"
            "Priority (Must/Should/Nice) | Roles Affected\n"
            "</use_case_template>\n\n"
            "<requirements>\n"
            "1. Write 4-6 use cases covering the main feature scenarios\n"
            "2. After the use cases, identify ONE non-obvious use case the team likely missed\n"
            "3. Every exception flow must describe a testable failure scenario\n"
            "</requirements>"
        ),
        "evaluation_rubric": (
            "Score this use case document prompt/output (0-25 each):\n"
            "1. Actor Coverage: Are all actors and their distinct goals addressed?\n"
            "2. Flow Completeness: Are main, alternative, and exception flows all present?\n"
            "3. Pre/Post Conditions: Are the system state requirements clearly documented?\n"
            "4. Priority & Insight: Is priority indicated, and did Claude surface a non-obvious use case?"
        ),
    },
    {
        "id": "req_nfr",
        "category": "requirements",
        "category_label": "Requirements",
        "icon": "🔍",
        "title": "Define Non-Functional Requirements",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "scenario": (
            "Your team often ships features that work functionally but have performance, "
            "security, or reliability issues discovered post-launch. "
            "Use Claude to define comprehensive non-functional requirements (NFRs) "
            "for an upcoming real-time chat feature so these issues are prevented."
        ),
        "context": (
            "The chat feature: real-time messaging between users, file attachment support, "
            "message history, notifications. Expected peak load: 10,000 concurrent users. "
            "The product serves enterprise clients with strict security requirements. "
            "GDPR compliance required. SLA target: 99.9% uptime."
        ),
        "what_makes_a_great_prompt": [
            "Insist on measurable thresholds for every NFR — tell Claude explicitly: 'Every NFR must include a specific, measurable threshold. Replace vague descriptions like \"fast\" or \"secure\" with concrete numbers: response time <200ms at p95, message delivery <500ms, file upload <30 seconds for files up to 25MB. If a threshold cannot be quantified, explain why and propose a proxy measure instead.'",
            "Ask for a Test Method column in the NFR table: 'Add a Test Method column: how would an engineer verify this NFR is met? Options include: automated load test, penetration test, manual audit, monitoring alert, static analysis, compliance audit.' NFRs without test methods are aspirations, not requirements.",
            "Structure NFRs by category in separate <nfr_category> tags: '<nfr_category name=\"Performance\">...</nfr_category><nfr_category name=\"Security\">...' This forces coverage of every category and makes the document easier to assign to the relevant engineering owners.",
            "Ask Claude to flag NFRs that require early architectural decisions: 'After the NFR table, write a section called \"Design-Time Constraints\" — NFRs that cannot be retrofitted and must be designed in from the start (e.g., end-to-end encryption architecture, WebSocket infrastructure). Flag each with which sprint they must be decided by.'",
            "Include GDPR compliance as specific requirements, not a general statement: 'GDPR requirements must be enumerated specifically: data residency rules, right to erasure implementation, data retention periods, consent requirements for message data. A general \"GDPR compliant\" NFR tells engineers nothing actionable.'",
        ],
        "model_prompt": (
            "You are a senior product manager defining non-functional requirements for an enterprise feature.\n\n"
            "<feature>\n"
            "Real-time chat: messaging, file attachments (up to 25MB), message history, "
            "push/email notifications. Peak load: 10,000 concurrent users. Enterprise B2B product.\n"
            "</feature>\n\n"
            "<constraints>\n"
            "GDPR compliance required | SLA target: 99.9% uptime | Enterprise security requirements | "
            "File types: images, PDFs, Office docs (no executables)\n"
            "</constraints>\n\n"
            "<nfr_table_columns>\n"
            "Category | NFR ID | Requirement | Measurable Threshold | Test Method | Priority | Design-Time? (yes/no)\n"
            "</nfr_table_columns>\n\n"
            "<categories_required>\n"
            "1. Performance (message delivery, response times, throughput)\n"
            "2. Scalability (concurrent users, growth headroom)\n"
            "3. Security (encryption, auth, access control, data handling)\n"
            "4. Reliability & Availability (uptime, failover, message durability)\n"
            "5. Compliance (specific GDPR articles — not just 'GDPR compliant'; data retention; right to erasure)\n"
            "</categories_required>\n\n"
            "<requirements>\n"
            "1. Every threshold must be a number — no vague terms\n"
            "2. Every Test Method must be specific (load test, pen test, audit, monitoring alert)\n"
            "3. After the table: list Design-Time Constraints — NFRs that cannot be retrofitted, with sprint deadline\n"
            "</requirements>"
        ),
        "evaluation_rubric": (
            "Score this NFR document prompt/output (0-25 each):\n"
            "1. Coverage: Are all 5 NFR categories (performance, security, reliability, scale, compliance) addressed?\n"
            "2. Measurability: Are requirements specific with numbers (e.g., <200ms, 99.9% uptime)?\n"
            "3. Test-Ready: Can each NFR be directly converted into an acceptance test?\n"
            "4. Risk Awareness: Are the hardest/most critical NFRs flagged for early attention?"
        ),
    },
    {
        "id": "req_definition_of_done",
        "category": "requirements",
        "category_label": "Requirements",
        "icon": "🔍",
        "title": "Create a Definition of Done",
        "difficulty": "beginner",
        "xp_reward": 50,
        "scenario": (
            "Your team keeps having 'done' arguments at sprint reviews — "
            "engineers say done, QA finds issues, stakeholders want more. "
            "Use Claude to create a comprehensive, team-agreed Definition of Done "
            "that prevents these disputes."
        ),
        "context": (
            "Your team: 4 engineers, 1 QA, 1 designer, 1 PM. "
            "You build a B2B SaaS product. Code reviews are manual (no automation yet). "
            "You do weekly deployments. You have a staging environment but limited test coverage. "
            "Past issues: untested edge cases, missing docs, UX inconsistencies post-launch."
        ),
        "what_makes_a_great_prompt": [
            "Tell Claude each past failure mode explicitly and ask it to trace each one to a DoD item: 'Our past failures: (1) untested edge cases in production (2) missing API documentation (3) UX inconsistencies not caught before launch. For each failure, create at least one DoD checklist item that would have caught it. Label each item with the failure it addresses.'",
            "Require binary yes/no items only — tell Claude why: 'Every DoD item must be answerable with yes or no before marking a story done. Subjective items like \"code is clean\" or \"design looks good\" are not allowed — replace them with \"Code review approved by one engineer\" and \"Designer sign-off received\". Binary items prevent the arguments you're trying to avoid.'",
            "Separate the DoD into 3 distinct tiers and define what each tier unlocks: 'Tier 1: Story Done (the story can move to QA). Tier 2: Sprint Done (the sprint can be demoed to stakeholders). Tier 3: Release Done (the code can go to production). Each tier must have role-specific checklists because different roles own different criteria.'",
            "Ask Claude to write role-specific checklists with accountability: 'Each tier must break into sub-checklists: Dev checklist | QA checklist | Design checklist | PM checklist. Every item must have a clear owner — if two roles can both claim ownership, it gets skipped in practice.'",
            "Ask Claude to write a conflict resolution clause: 'Add a \"What to do when there is disagreement\" section: a short rule for how to resolve disputes about whether a DoD item is met. For example: \"PM has final say on Story Done; Engineering Lead has final say on Release Done.\" Ambiguous authority causes the same arguments as vague criteria.'",
        ],
        "model_prompt": (
            "You are a senior product manager creating a Definition of Done to eliminate sprint review disputes.\n\n"
            "<team>\n"
            "4 engineers, 1 QA, 1 designer, 1 PM | Weekly deployments | Staging environment | Limited test automation\n"
            "</team>\n\n"
            "<past_failures>\n"
            "1. Untested edge cases shipped to production (discovered by customers)\n"
            "2. API documentation missing when features launched (blocked integrators)\n"
            "3. UX inconsistencies (button styles, error messages) not caught before launch\n"
            "</past_failures>\n\n"
            "<requirements>\n"
            "1. Three tiers: Story Done (moves to QA) | Sprint Done (demoable) | Release Done (production-ready)\n"
            "2. Each tier: separate checklists for Dev | QA | Design | PM\n"
            "3. Every item must be binary (yes/no) — no subjective terms\n"
            "4. Trace each past failure to at least one DoD item (label it with the failure it prevents)\n"
            "5. Conflict resolution clause: who has final say at each tier when there is disagreement\n"
            "</requirements>\n\n"
            "<output_format>\n"
            "Format as a Confluence checklist template. Each item uses '- [ ]' checkbox format.\n"
            "Section headers: ## Story Done | ## Sprint Done | ## Release Done\n"
            "Sub-headers: ### Dev | ### QA | ### Design | ### PM\n"
            "</output_format>"
        ),
        "evaluation_rubric": (
            "Score this Definition of Done prompt/output (0-25 each):\n"
            "1. Tiering: Are there clear, distinct levels (Story / Sprint / Release)?\n"
            "2. Role Clarity: Are checklists broken out by role responsibility?\n"
            "3. Binariness: Are all items yes/no checkable (not subjective)?\n"
            "4. Problem-Solving: Does the DoD directly address the stated past failure modes?"
        ),
    },
    {
        "id": "req_change_request",
        "category": "requirements",
        "category_label": "Requirements",
        "icon": "🔍",
        "title": "Document a Scope Change",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "scenario": (
            "Mid-sprint, the CEO wants to add a feature: 'Can we also send each customer an "
            "automated SMS when their subscription auto-renews? I think it could reduce churn — "
            "we're seeing 2% day-1 cancellations from people surprised by the charge.' "
            "This is a scope change that will impact the current sprint. "
            "Use Claude to write a proper Change Request document."
        ),
        "context": (
            "Current sprint has 3 days left. The SMS feature requires: Twilio integration, "
            "new database table, GDPR consent mechanism, template design. "
            "Estimated: 5-7 days of engineering work. "
            "This was not in the original scope and will delay the sprint goal. "
            "The CEO wants it 'this sprint if possible.'"
        ),
        "what_makes_a_great_prompt": [
            "Lead with impact, not the request — tell Claude to structure the document this way: 'Open with the sprint impact, not the change description. The reader already knows what was requested. What they need to understand immediately is what accepting it costs: 3 days left + 5-7 days of work = sprint goal at risk.' Impact-first framing produces faster decisions.",
            "Ask Claude to write three options with an explicit recommendation, not a balanced hedge: 'Present exactly 3 options (accept now / defer to next sprint / MVP-scoped version). For each, write: Time | Cost | Sprint Goal Impact | Recommendation (yes/no). End with a single recommended option. Do NOT write \"both options have merit\" — that's not a recommendation, it's a refusal to decide.'",
            "Give Claude an explicit tone contrast, not just a vague instruction: 'The CEO requested this — the document must be respectful and acknowledge the business case. NOT: \"This is impossible\" (sounds like refusal). NOT: \"We can try\" (sounds like a yes when it isn't). YES: \"To deliver this with the quality it deserves, we need 5-7 days — here are your three options.\" The goal is a crisp decision, not a refusal or a hedge.'",
            "Ask for the change to be documented against the original scope: 'Include a section called \"Original Sprint Scope\" listing the committed stories and their status. This contextualizes why adding work mid-sprint is impactful — without this context, the CEO may not realize what they're asking the team to trade off.'",
            "Specify the decision needed as a single yes/no question with a deadline: 'End with a highlighted \"Decision Needed\" box: one yes/no question, the name of the decision maker, and a deadline (e.g., today by 3pm — after which the team continues with the original scope by default).' A default outcome prevents decisions from stalling.",
        ],
        "model_prompt": (
            "You are a senior product manager writing a formal Change Request document.\n\n"
            "<change_request>\n"
            "Request: Add automated SMS renewal notification (Twilio integration, new DB table, GDPR consent, template design)\n"
            "Requester: CEO\n"
            "Requested timing: 'This sprint if possible'\n"
            "Engineering estimate: 5-7 days\n"
            "Current sprint status: 3 days remaining, sprint goal at risk if scope added\n"
            "</change_request>\n\n"
            "<original_sprint_scope>\n"
            "Sprint goal: Complete payment refactor + notification v2\n"
            "Stories: 6 committed (22 of 24 points), 2 not yet started\n"
            "</original_sprint_scope>\n\n"
            "<output_format>\n"
            "1. Sprint Impact (FIRST section — what accepting this costs in concrete terms)\n"
            "2. Change Description (what was requested and its business value — 2 sentences)\n"
            "3. Original Sprint Scope (what was committed and current status)\n"
            "4. Implementation Requirements (high-level bullet list, no longer than 5 items)\n"
            "5. Options Analysis (table: Option | Engineering Time | Sprint Goal Impact | Recommended?)\n"
            "   Option A: Accept now | Option B: Next sprint | Option C: MVP scope (template only, no Twilio)\n"
            "6. Recommendation (name Option B or C — explain in 3 bullets — no hedging)\n"
            "7. Decision Needed [highlighted box]: one yes/no question | Decision Maker: CEO | Deadline: today 3pm | Default if no response: continue with original scope\n"
            "</output_format>\n\n"
            "Tone: respectful and solution-oriented. Acknowledge the business value. Be direct about the impact."
        ),
        "evaluation_rubric": (
            "Score this change request prompt/output (0-25 each):\n"
            "1. Impact Honesty: Is the sprint impact and risk stated clearly without sugar-coating?\n"
            "2. Options Quality: Are 3 viable options presented with clear tradeoffs?\n"
            "3. Recommendation: Is there a clear, justified recommendation (not wishy-washy)?\n"
            "4. Professionalism: Does it maintain a constructive tone while being direct about the impact?"
        ),
    },
]

CATEGORIES = {
    "jira": {"label": "Jira & Backlog", "icon": "🎯", "color": "#0052CC"},
    "confluence": {"label": "Confluence & Docs", "icon": "📄", "color": "#172B4D"},
    "stakeholder": {"label": "Stakeholder Comms", "icon": "📧", "color": "#00875A"},
    "devteam": {"label": "Dev Team Collab", "icon": "💻", "color": "#6554C0"},
    "requirements": {"label": "Requirements", "icon": "🔍", "color": "#FF5630"},
}

LEVELS = [
    {"level": 1, "name": "AI Apprentice", "min_xp": 0, "max_xp": 200, "color": "#718096"},
    {"level": 2, "name": "Prompt Explorer", "min_xp": 200, "max_xp": 500, "color": "#4299E1"},
    {"level": 3, "name": "AI Practitioner", "min_xp": 500, "max_xp": 1000, "color": "#48BB78"},
    {"level": 4, "name": "Claude Expert", "min_xp": 1000, "max_xp": 2000, "color": "#ED8936"},
    {"level": 5, "name": "AI Champion", "min_xp": 2000, "max_xp": 9999999, "color": "#9F7AEA"},
]

BADGES = {
    "first_challenge": {
        "id": "first_challenge",
        "name": "First Steps",
        "description": "Completed your first challenge",
        "icon": "🌱",
    },
    "jira_master": {
        "id": "jira_master",
        "name": "Jira Master",
        "description": "Completed all Jira & Backlog challenges",
        "icon": "🎯",
    },
    "doc_wizard": {
        "id": "doc_wizard",
        "name": "Doc Wizard",
        "description": "Completed all Confluence & Docs challenges",
        "icon": "📄",
    },
    "communicator": {
        "id": "communicator",
        "name": "Communicator",
        "description": "Completed all Stakeholder Comms challenges",
        "icon": "📧",
    },
    "team_player": {
        "id": "team_player",
        "name": "Team Player",
        "description": "Completed all Dev Team challenges",
        "icon": "💻",
    },
    "requirements_pro": {
        "id": "requirements_pro",
        "name": "Requirements Pro",
        "description": "Completed all Requirements challenges",
        "icon": "🔍",
    },
    "perfectionist": {
        "id": "perfectionist",
        "name": "Perfectionist",
        "description": "Scored 95 or higher on any challenge",
        "icon": "💎",
    },
    "high_achiever": {
        "id": "high_achiever",
        "name": "High Achiever",
        "description": "Scored 80+ on 5 different challenges",
        "icon": "⭐",
    },
    "speed_demon": {
        "id": "speed_demon",
        "name": "Speed Demon",
        "description": "Completed 3 challenges in a single day",
        "icon": "⚡",
    },
    "completionist": {
        "id": "completionist",
        "name": "Completionist",
        "description": "Completed all 20 challenges",
        "icon": "🏆",
    },
}


def get_level(xp: int) -> dict:
    for level_info in reversed(LEVELS):
        if xp >= level_info["min_xp"]:
            return level_info
    return LEVELS[0]


def get_xp_reward(score: int, base_reward: int) -> int:
    if score >= 90:
        multiplier = 1.5
    elif score >= 75:
        multiplier = 1.2
    elif score >= 50:
        multiplier = 1.0
    elif score >= 30:
        multiplier = 0.3
    else:
        multiplier = 0.0
    return round(base_reward * multiplier)
