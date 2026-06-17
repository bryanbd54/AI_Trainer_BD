COPILOT_CHALLENGES = [
    # ── OUTLOOK COPILOT ────────────────────────────────────────────────────────
    {
        "id": "copilot_outlook_thread_summary",
        "category": "outlook",
        "category_label": "Outlook Copilot",
        "icon": "📧",
        "title": "Summarize a Stakeholder Thread",
        "difficulty": "beginner",
        "xp_reward": 50,
        "track": "copilot",
        "scenario": (
            "You returned from a 2-day offsite to find a 14-message email thread between your VP, "
            "engineering lead, and two external vendors arguing about a Q4 delivery date. "
            "Your VP wants your assessment in 30 minutes. Use Outlook Copilot to catch up "
            "and extract exactly what matters."
        ),
        "context": (
            "The thread covers conflicting commitments about when a data integration will be ready. "
            "Two vendors gave different delivery dates. There are side-comments about budget "
            "that your VP flagged. You've been cc'd on everything but haven't read a single message."
        ),
        "what_makes_a_great_prompt": [
            "In Outlook, Copilot's 'Summarize by Copilot' banner appears automatically on long threads — but for smarter extraction, open the Copilot chat pane and ask targeted questions rather than using the default button. 'What did each party commit to?' extracts decisions; the banner extracts narrative. The chat pane is where the real power lives.",
            "Apply Microsoft's Source element: name the specific senders you care about. 'Summarize this thread, focusing on commitments made by the two vendors' narrows Copilot's attention to the most relevant content. Without a source constraint, Copilot weights all messages equally, diluting the signal.",
            "Ask Copilot to separate confirmed commitments from open questions — these are qualitatively different and Copilot blends them without explicit instruction. 'List confirmed commitments separately from items still under discussion.' This distinction is exactly what you need to brief your VP convincingly.",
            "Ask about your own obligations separately: 'What actions or questions were directed specifically to me in this thread?' This is the fastest way to triage inbox debt — reading 14 messages to find your name takes 10 minutes; asking Copilot takes 5 seconds.",
            "Always follow up the initial summary with 'What is still unresolved?' Default summaries imply false consensus — this follow-up explicitly surfaces the gaps you need to address before your VP meeting.",
        ],
        "model_prompt": (
            "Goal: Summarize this 14-message email thread so I can brief my VP in 30 minutes.\n\n"
            "Context: I've been at an offsite and missed this entire thread. It involves my VP, "
            "our engineering lead, and two external vendors (Acme Inc and DataCo) debating the "
            "Q4 delivery date for a data integration. My VP flagged budget concerns in at least "
            "one message.\n\n"
            "What I need:\n"
            "1. Confirmed commitments from each party (name + commitment)\n"
            "2. Open questions and unresolved disagreements\n"
            "3. Any budget-related items my VP flagged\n"
            "4. Actions or questions directed specifically to me\n\n"
            "Format: bullet points grouped by the 4 categories above. Flag anything time-sensitive "
            "with ⚠️. Keep it under 200 words — I have 30 minutes to prepare."
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Is the task specific and actionable? (0=vague; 25=specific goal with clear deliverable and time constraint)\n"
            "2. Context (0-25): Is enough business background provided — who's involved, why it matters, what the user needs to do with the output? (0=no context; 25=rich context enabling Copilot to prioritize the right signal)\n"
            "3. Source (0-25): Does the prompt direct Copilot to the right content — specific senders, timeframes, or flagged items? (0=no source guidance; 25=specific source direction with named parties)\n"
            "4. Expectations (0-25): Are format, output structure, length, and organization requirements stated? (0=no format; 25=explicit categories, length limit, and urgency signals)"
        ),
    },
    {
        "id": "copilot_outlook_delay_draft",
        "category": "outlook",
        "category_label": "Outlook Copilot",
        "icon": "📧",
        "title": "Draft a Delay Email with Copilot Coaching",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "track": "copilot",
        "scenario": (
            "The mobile app launch you own is slipping 2 weeks. It affects a co-marketing campaign "
            "your VP of Marketing already announced publicly to partners. You need to tell her — "
            "and she won't be happy. Use Copilot to draft the email and improve it with Coaching "
            "before sending."
        ),
        "context": (
            "Root cause: a third-party payment library incompatibility discovered in UAT — not an "
            "internal team failure. Original launch: October 10. New date: October 24. "
            "Impact: the co-marketing email campaign must pause; partner announcement needs updating. "
            "Mitigation: beta access for key partners starting October 14."
        ),
        "what_makes_a_great_prompt": [
            "Specify tone AND anti-tone in the Expectations element: 'Tone: direct and accountable. NOT defensive (don't over-explain the technical cause). NOT apologetic to the point of groveling (maintain confidence).' The contrast pair is more directive than describing tone positively alone — it tells Copilot what to avoid while still giving it a clear target.",
            "Put the most important fact first in the Context element: 'The most important fact is the new launch date (Oct 24). This should appear in sentence 1.' Without this, Copilot may bury the date in paragraph 2 after background context — which frustrates executive readers who need the key fact immediately.",
            "Use Coaching by Copilot after drafting: in the compose window, click 'Coaching by Copilot' and ask specific questions — 'Does this sound defensive? Does it give the marketing team enough to update the partner announcement?' Specific coaching questions produce specific, actionable suggestions.",
            "Add a length constraint to the Expectations element: 'Under 200 words.' Copilot defaults to longer, more hedged drafts — a word limit forces the kind of executive-appropriate brevity that VP emails require.",
            "Ask Copilot to draft the subject line separately: 'Draft a subject line that names the new date directly (not \"Important Update\" — something like \"Mobile Launch Rescheduled to October 24\").' Subject lines drive whether executive emails get acted on or re-opened later.",
        ],
        "model_prompt": (
            "Goal: Draft an email to my VP of Marketing about a 2-week delay to our mobile app "
            "launch that affects her publicly announced co-marketing campaign.\n\n"
            "Context: Root cause is a third-party library incompatibility found in UAT — this is "
            "a vendor issue, not our team's failure. Original launch: October 10. New date: "
            "October 24. Her co-marketing email campaign to partners needs to pause. Mitigation: "
            "we can offer beta access to key partners starting October 14.\n\n"
            "Tone: Direct and accountable. NOT defensive — limit technical explanation to one "
            "sentence. NOT apologetic to the point of groveling. Confident.\n\n"
            "Expectations:\n"
            "- Under 200 words\n"
            "- Start sentence 1 with the new date: 'The mobile app launch is rescheduled to October 24.'\n"
            "- Include: what changed, the mitigation (beta access Oct 14), one specific ask from her\n"
            "- End with a decision request: what I need her to decide by end of day\n"
            "- Also draft a subject line that names the new date directly"
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Is the task specific — right audience, right purpose, not just 'write an email'?\n"
            "2. Context (0-25): Does it provide business situation, root cause, impact on the recipient, and mitigation details Copilot needs to draft accurately?\n"
            "3. Source (0-25): Are specific facts (exact dates, impacts, mitigation details) provided so Copilot has real content to work with rather than generic language?\n"
            "4. Expectations (0-25): Are tone (and anti-tone), length, required content elements, and the subject line ask all specified?"
        ),
    },
    {
        "id": "copilot_outlook_meeting_convert",
        "category": "outlook",
        "category_label": "Outlook Copilot",
        "icon": "📧",
        "title": "Convert an Email Thread to a Meeting Invite",
        "difficulty": "beginner",
        "xp_reward": 50,
        "track": "copilot",
        "scenario": (
            "A 9-message email thread titled 'Aligning on Q4 scope' has been going in circles "
            "for 3 days. Five people are involved. Two opposing positions have emerged. Nothing "
            "is being resolved asynchronously. Use Copilot in Outlook to turn this into a "
            "focused, decision-making meeting invite."
        ),
        "context": (
            "Participants: PM lead, CTO, Head of Design, Head of Data, and a business stakeholder. "
            "Two camps: one wants to cut features to hit the October deadline; the other wants to "
            "extend the deadline to preserve the features. A 45-minute decision meeting is needed "
            "this week."
        ),
        "what_makes_a_great_prompt": [
            "Outlook Copilot's 'Schedule with Copilot' feature (calendar icon in the compose toolbar) auto-generates a meeting from your thread — it pulls attendees and drafts an agenda. But the auto-generated agenda is often generic. Open the Copilot chat pane to override it with decision-framed agenda items instead.",
            "Tell Copilot this is a decision meeting, not a status meeting, in the Goal element: 'Agenda items should be phrased as decisions to make, not topics to discuss.' The difference between 'Discuss Q4 scope' and 'Decide: cut features or extend deadline?' is the difference between a meeting that ends in more discussion and one that ends in a decision.",
            "Include pre-read requirements in the Expectations element: 'Add a Pre-read section with 2 questions attendees should answer before joining.' Pre-reads transform meeting quality — and writing them forces you to clarify what decision you're actually trying to make.",
            "Ask Copilot to add a Decision Log template to the invite body: 'Add a blank Decision Log table (Decision | Owner | Date) for use during the meeting.' This one addition makes it far more likely decisions get captured — it changes how people approach the meeting.",
            "Ask Copilot to summarize the email conflict in the invite background section: 'Include a 2-sentence background explaining why this meeting was called, based on the thread.' Attendees who joined the thread late or not at all need context — otherwise they arrive unprepared.",
        ],
        "model_prompt": (
            "Goal: Create a 45-minute decision meeting invite for the Q4 scope alignment discussion "
            "this week. This is a decision meeting, not a discussion — we must leave with a "
            "documented decision.\n\n"
            "Context: A 9-message email thread has circled for 3 days. Two opposing positions: "
            "(1) cut features to hit the October deadline, (2) extend deadline to keep features. "
            "Five attendees: PM lead, CTO, Head of Design, Head of Data, business stakeholder. "
            "No consensus reached asynchronously.\n\n"
            "Expectations for the meeting invite:\n"
            "- Subject: Names the decision, not the topic ('Q4 Scope Decision Meeting' not 'Q4 Scope Discussion')\n"
            "- Background section: 2 sentences explaining why this meeting is needed now\n"
            "- Agenda: 3 items maximum, each phrased as a decision ('Decide: X' — not 'Discuss X')\n"
            "- Pre-read: 2 questions attendees should be prepared to answer when they arrive\n"
            "- Decision Log template: blank table (Decision | Owner | Date) for note-taking during the meeting\n"
            "- Suggest 3 possible time slots this week (Tuesday–Thursday, 30-minute windows)"
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Is the meeting type (decision, not discussion), duration, and required outcome specifically defined?\n"
            "2. Context (0-25): Does it provide the attendees, the two opposing positions, and why async failed?\n"
            "3. Source (0-25): Does the prompt reference the email thread and provide enough facts for the agenda?\n"
            "4. Expectations (0-25): Are the invite format requirements, decision-framed agenda style, and add-ons (pre-read, decision log, time slots) specified?"
        ),
    },
    {
        "id": "copilot_outlook_tone_control",
        "category": "outlook",
        "category_label": "Outlook Copilot",
        "icon": "📧",
        "title": "One Message, Three Audiences",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "track": "copilot",
        "scenario": (
            "The Q4 roadmap review meeting is moving from Friday to Tuesday at 2pm due to a "
            "scheduling conflict. Three groups need to hear about it — but each needs something "
            "different. Use Copilot to efficiently draft three tailored versions of this message "
            "in a single prompt."
        ),
        "context": (
            "Recipients: (1) CEO — strategic, needs to know this doesn't delay any external "
            "commitments. (2) Engineering lead — logistical, needs the new time and whether the "
            "dial-in room link changes. (3) Your immediate team — casual, just needs the time change. "
            "The agenda is unchanged. Do NOT mention whose scheduling conflict caused the move."
        ),
        "what_makes_a_great_prompt": [
            "Use parallel structure in the Expectations element to request multiple versions in one prompt: 'Write 3 versions: (1) CEO: 2 sentences, strategic (2) Engineering lead: 3 sentences, logistical (3) Team: casual, 2 sentences.' Copilot produces all three in sequence — far faster than three separate prompts.",
            "Outlook's Custom Instructions (Settings → Copilot → Custom Instructions) let you set standing tone preferences for all drafts — your name, default greeting, phrases to avoid. Set these once and Copilot stops adding 'I hope this email finds you well' permanently. This challenge is a perfect reason to configure them.",
            "Give Copilot negative vocabulary constraints in the Expectations element: 'No filler phrases: I hope this email finds you well / Please let me know if you have any questions. Start every version with the key fact.' These specific exclusions eliminate Copilot's most common generic openers reliably.",
            "Include the sensitive information constraint in the Context element: 'Do not mention or imply whose conflict caused the reschedule. Frame it as a general scheduling conflict affecting the group.' Copilot respects explicit information constraints — it won't infer what to exclude on its own.",
            "Ask Copilot to self-evaluate after generating: 'After writing the 3 versions, flag any sentence in any version that sounds like generic AI language rather than a real PM's message.' This self-critique step catches generic phrases that survive the initial draft.",
        ],
        "model_prompt": (
            "Goal: Draft 3 versions of a message communicating that the Q4 roadmap review moved "
            "from this Friday to Tuesday at 2pm.\n\n"
            "Context: The meeting moved due to a scheduling conflict — do NOT say or imply whose "
            "conflict it was. The agenda is unchanged. All versions must convey: meeting moved to "
            "Tuesday 2pm, agenda unchanged, please update your calendar.\n\n"
            "Version 1 — CEO email (2 sentences):\n"
            "- Strategic framing: note that this doesn't affect any external commitments or Q4 delivery dates\n"
            "- No preamble, no pleasantries\n\n"
            "Version 2 — Engineering lead email (3 sentences):\n"
            "- New time (Tuesday 2pm), whether dial-in/room info changes (note it's TBD if unknown), agenda unchanged\n"
            "- Direct and logistical\n\n"
            "Version 3 — Team Slack message (casual, 2 sentences):\n"
            "- Friendly, informal, just the facts\n\n"
            "Rules for all 3:\n"
            "- Start with the key fact (date change), not pleasantries\n"
            "- No 'I hope this email finds you well' or 'Please let me know if you have any questions'\n"
            "- Under 75 words each\n"
            "- After drafting all 3: flag any sentence that sounds like AI-generated filler rather than a real PM's voice"
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Are the 3 versions, their audiences, and their distinct purposes clearly defined?\n"
            "2. Context (0-25): Are the audience differences, the sensitive information constraint, and the shared key facts all provided?\n"
            "3. Source (0-25): Are the specific facts Copilot needs for each version (dates, constraints, agenda status) included?\n"
            "4. Expectations (0-25): Are length, tone, prohibited phrases, and the post-generation self-review specified for all 3 versions?"
        ),
    },

    # ── TEAMS COPILOT ──────────────────────────────────────────────────────────
    {
        "id": "copilot_teams_meeting_recap",
        "category": "teams",
        "category_label": "Teams Copilot",
        "icon": "💬",
        "title": "Extract Intelligence from a Meeting Recap",
        "difficulty": "beginner",
        "xp_reward": 50,
        "track": "copilot",
        "scenario": (
            "You just finished a 75-minute quarterly product review with 14 attendees. Your calendar "
            "shows 3 more back-to-back meetings starting in 20 minutes. You need the key decisions, "
            "all action items with owners, and unresolved issues — in under 5 minutes. "
            "Use Teams Copilot's Intelligent Recap to extract what you need."
        ),
        "context": (
            "The meeting covered: Q4 roadmap finalization, a decision on whether to delay the "
            "mobile feature, resource allocation for two competing projects, and a go-to-market "
            "timing debate that didn't fully resolve. Your CEO was on the call and made at "
            "least two commitments."
        ),
        "what_makes_a_great_prompt": [
            "Intelligent Recap is auto-generated after the meeting — find it in the 'Recap' tab of the meeting chat or by opening the meeting from your Teams calendar. The default recap is a good start, but the real value comes from follow-up questions in the Copilot pane. Don't stop at the summary.",
            "Ask for decisions with attribution: 'List all decisions made in this meeting. For each: what was decided, who proposed it, any conditions attached.' Decision attribution prevents the most common post-meeting dispute: 'I thought Sarah was deciding that, not John.' Copilot extracts ownership from the transcript.",
            "Ask for action items in a specific format: 'List all action items: owner + action (verb-first) + due date. If no due date was stated, write not specified — do not infer or guess dates.' The explicit 'do not infer' instruction prevents Copilot from adding plausible-but-wrong dates that create accountability confusion.",
            "Ask whether contentious items were actually resolved: 'Was the go-to-market timing discussion resolved in this meeting? If yes, what was agreed? If no, what positions remained open at the end?' This targeted query surfaces the items the default summary typically softens into false closure.",
            "Ask about the CEO's commitments specifically: 'Did the CEO make any commitments or express clear preferences in this meeting? Quote the relevant transcript.' Attribution to senior leaders matters — ask Copilot to cite the transcript rather than summarize, so you can verify.",
        ],
        "model_prompt": (
            "Goal: Give me the essential output from this quarterly product review in under 5 minutes "
            "so I can move directly to my next meeting.\n\n"
            "Context: 75-minute meeting with 14 people including the CEO. Topics: Q4 roadmap "
            "finalization, mobile feature delay decision, resource allocation, go-to-market timing "
            "(this last item was contentious and may not have fully resolved).\n\n"
            "What I need:\n"
            "1. All decisions made — format: Decision | Who proposed it | Any conditions attached\n"
            "2. All action items — format: Owner | Action (verb-first) | Due date stated "
            "(write 'not specified' if no date was mentioned — do not guess)\n"
            "3. Go-to-market timing: was it resolved? If yes, what was decided? "
            "If no, what positions are still open?\n"
            "4. Any commitments or stated preferences from the CEO specifically\n\n"
            "Format: grouped by the 4 categories. Flag anything that requires action before EOD with ⚠️. "
            "Under 300 words total."
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Is the task specific — 5-minute brief, 4 defined outputs, time pressure stated?\n"
            "2. Context (0-25): Does it describe the meeting scope, key attendees, topics covered, and the contentious item?\n"
            "3. Source (0-25): Does the prompt direct Copilot to specific content — the unresolved item, CEO specifically, the transcript as source?\n"
            "4. Expectations (0-25): Are format requirements, output categories, attribution rules, inference prohibition, and length specified?"
        ),
    },
    {
        "id": "copilot_teams_mid_meeting",
        "category": "teams",
        "category_label": "Teams Copilot",
        "icon": "💬",
        "title": "Ask Mid-Meeting Questions",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "track": "copilot",
        "scenario": (
            "You've just joined a 90-minute executive product strategy meeting 40 minutes late "
            "due to an overrunning call. You have two agenda items coming up in 30 minutes "
            "and need to contribute meaningfully. Use Teams Copilot mid-meeting to get caught "
            "up without disrupting the flow."
        ),
        "context": (
            "The meeting is about Q4 product strategy. You own 'international expansion' and "
            "'enterprise tier' — both scheduled in the second half. From the pre-meeting doc, "
            "you know there was a planned headcount debate. You have no idea what's been decided "
            "or what the group's current mood or alignment looks like."
        ),
        "what_makes_a_great_prompt": [
            "Open Copilot in the Teams meeting side panel by clicking the Copilot icon in the meeting toolbar. Mid-meeting Copilot draws ONLY from the live transcript — it cannot access your files, emails, or previous meetings. All your questions must be anchored to 'what has been said in this meeting' — any other framing will get you an error or an uninformed response.",
            "Ask for a chronological timeline summary to orient yourself quickly: 'Summarize what's been discussed in this meeting so far, in order, in 5 bullet points.' This is faster than asking for a full recap and gives you a map of where the meeting has been — so you know where you're walking into.",
            "Ask about your specific agenda items: 'Have international expansion or enterprise tier been mentioned in this meeting so far? If so, what was said?' Your topics may have come up earlier than scheduled — Copilot tells you in 10 seconds what would take you 40 minutes of guessing.",
            "Ask for the state of alignment: 'Is the group aligned on Q4 strategy so far, or are there active unresolved disagreements? What are they?' Knowing whether you're walking into consensus or ongoing conflict changes everything about how you present your items.",
            "Ask Copilot to generate a question for you: 'Based on the discussion so far, what is the most important open question related to international expansion that hasn't been addressed yet?' This creative use of mid-meeting Copilot helps you contribute meaningfully even when arriving 40 minutes late.",
        ],
        "model_prompt": (
            "Goal: Get me caught up on a meeting I joined 40 minutes late so I can contribute "
            "meaningfully to my agenda items in the next 30 minutes.\n\n"
            "Context: This is a Q4 executive product strategy meeting. I own two agenda items: "
            "international expansion and enterprise tier, both scheduled in the second half. "
            "I know a headcount debate was planned. I have no visibility into what has been "
            "discussed or decided.\n\n"
            "What I need (answer ONLY from what has been said in this meeting so far — "
            "do not add outside context):\n"
            "1. Chronological summary: what topics were covered in order, in 5 bullet points\n"
            "2. Decisions made so far: what has been agreed on (if anything)\n"
            "3. Current disagreements: any active unresolved issues?\n"
            "4. My topics: have international expansion or enterprise tier been mentioned? "
            "If so, what was said?\n"
            "5. Suggested question: what is the most important open question about "
            "international expansion I could raise to contribute constructively?\n\n"
            "Important: base all answers only on this meeting's transcript."
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Is the task specific — catch-up for late joiner, 5 defined outputs, 30-minute window?\n"
            "2. Context (0-25): Does it explain the meeting type, topics owned, and the information gap?\n"
            "3. Source (0-25): Does the prompt correctly constrain Copilot to transcript-only — critical for mid-meeting accuracy?\n"
            "4. Expectations (0-25): Are output format, scope boundaries ('this meeting only'), and specific topics (international expansion, enterprise) defined?"
        ),
    },
    {
        "id": "copilot_teams_chat_catchup",
        "category": "teams",
        "category_label": "Teams Copilot",
        "icon": "💬",
        "title": "Catch Up on a Teams Channel",
        "difficulty": "beginner",
        "xp_reward": 50,
        "track": "copilot",
        "scenario": (
            "You were at a client site for 3 days and missed 78 messages in the 'Q4 Launch' "
            "Teams channel. It's Monday morning and standup is in 15 minutes. You need to know "
            "what happened, what requires your input, and whether anything is blocking the team — "
            "in under 5 minutes. Use Teams Copilot to triage the backlog."
        ),
        "context": (
            "The Q4 Launch channel covers: feature dev status, a QA process that's running behind, "
            "a design review that was completed, and ongoing discussion about the launch "
            "communication plan. Two team members have been asking questions that may be waiting "
            "on PM input. Marketing sent a launch brief that no one responded to."
        ),
        "what_makes_a_great_prompt": [
            "In Teams, open the channel and click the Copilot icon to access chat summarization. Always specify a timeframe: 'Summarize the last 3 days of conversation in this channel.' Without a timeframe, Copilot may summarize a shorter window and miss the messages you most need to catch up on.",
            "Ask Copilot to filter for items that need your attention specifically: 'What messages mention my name, ask a question that hasn't been answered, or appear to be waiting on PM input?' This targeted extraction is the highest-ROI Teams chat Copilot query — reading 78 messages to find your name takes 20 minutes; asking Copilot takes 10 seconds.",
            "Ask for open questions separately from decisions: 'What questions were posted in this channel in the last 3 days that haven't received an answer?' Questions that get buried without a response are a major source of team blockers — this query surfaces them explicitly.",
            "Ask for the most urgent item: 'What is the single most time-sensitive thing I need to address today, based on the last 3 days of this channel?' This uses Copilot's ability to detect urgency signals ('blocked,' 'waiting on,' 'need by today') to immediately triage your morning.",
            "Close the loop on specific items in the Context: 'Was the marketing launch brief acknowledged? Did anyone respond to it?' Asking about specific known items produces more reliable answers than asking Copilot to identify all important items from scratch.",
        ],
        "model_prompt": (
            "Goal: Triage 78 messages in the Q4 Launch channel that I missed over 3 days. "
            "Standup in 15 minutes — I need the essentials in under 5 minutes.\n\n"
            "Context: This channel covers feature dev, QA progress (I know it's behind), "
            "a design review (I think it completed), and the launch comms plan. I'm the PM. "
            "Marketing sent a launch brief. I've been at a client site since Thursday.\n\n"
            "From the last 3 days:\n"
            "1. Key decisions made (concise list)\n"
            "2. Messages mentioning my name or waiting on PM input\n"
            "3. Open questions posted to the group that haven't been answered\n"
            "4. The most urgent item I need to address today\n"
            "5. The marketing launch brief — was it acknowledged? Any responses?\n\n"
            "Format: bullet points per section. Flag anything I must respond to before 10am with ⚠️. "
            "Under 250 words total."
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Is the triage task defined — 5-minute limit, 15-minute standup, 5 specific outputs?\n"
            "2. Context (0-25): Does it describe the channel's scope, PM role, known items (QA, design review, marketing brief)?\n"
            "3. Source (0-25): Is the timeframe (3 days), specific channel content, and named items (marketing brief) cited?\n"
            "4. Expectations (0-25): Are the 5 output categories, format, urgency flagging (⚠️), and length limit specified?"
        ),
    },
    {
        "id": "copilot_teams_compose",
        "category": "teams",
        "category_label": "Teams Copilot",
        "icon": "💬",
        "title": "Compose a Difficult Team Message",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "track": "copilot",
        "scenario": (
            "You need to tell the engineering team that the reporting export feature they spent "
            "3 weeks building will not be in the Q4 release. The decision was made by leadership "
            "for scope reasons. The team is proud of this work and this message could demoralize "
            "them if poorly handled. Use Copilot Compose to draft a message that delivers the "
            "news while preserving morale."
        ),
        "context": (
            "The feature is functionally complete but was cut for scope reasons — Q4 focus is "
            "on stabilization. The feature will be prioritized for Q1 (a real commitment, not "
            "a hope). Three engineers worked on it. They were not involved in the cut decision "
            "and will be surprised. The message goes in the Engineering team channel."
        ),
        "what_makes_a_great_prompt": [
            "Use Copilot Compose in Teams (click the Copilot icon in the message compose box) and describe what you want — or paste a rough draft to refine. For difficult messages, describing the transformation you want is more reliable than just asking for a draft: 'Rewrite this message to be transparent while preserving morale' produces better results than 'write a message about cutting a feature.'",
            "Give Copilot the emotional transformation you need in the Goal: 'Draft a message that delivers difficult news (feature cut) while acknowledging the team's work and maintaining morale.' Without emotional framing, Copilot's rewrite focuses on clarity and brevity — missing the human dimension entirely.",
            "Specify what must be included vs. excluded in the Context: 'Include: acknowledgment of 3 weeks of work, the business reason (scope management, not quality concerns), Q1 commitment. Do NOT include: any suggestion that Q1 might also slip.' Explicit inclusion/exclusion controls produce complete, accurate messages.",
            "Ask for a tone transformation, not just content: 'Current tone is top-down and final. Rewrite as collaborative — the team deserves context, not just a decision.' Tone transformation instructions produce fundamentally different outputs than content-only instructions.",
            "Specify the channel format in Expectations: 'Teams channel message, under 150 words. No passive voice. No hedge phrases (unfortunately, I know this is disappointing) — be direct and respectful.' Passive voice and hedge phrases are the two most common ways difficult messages go wrong; naming them explicitly prevents them.",
        ],
        "model_prompt": (
            "Goal: Draft a Teams channel message to the engineering team announcing that the "
            "reporting export feature is cut from Q4 scope.\n\n"
            "Context:\n"
            "- The feature is functionally complete — this is a scope management decision, not "
            "a quality concern\n"
            "- Decision made by leadership; the team was not involved\n"
            "- Feature is committed for Q1 — this is a real commitment, not 'maybe'\n"
            "- Three engineers worked on this for 3 weeks\n"
            "- The team will be surprised and potentially demoralized\n\n"
            "The message must:\n"
            "1. Acknowledge the team's work specifically (not generic 'great job everyone')\n"
            "2. State the business reason clearly (scope and focus, not their quality)\n"
            "3. Confirm the Q1 commitment as firm\n"
            "4. End with a specific next step (when will we discuss Q1 prioritization?)\n\n"
            "Expectations: Teams channel message, under 150 words. Direct and respectful — "
            "not cold, not apologetic. No passive voice. No hedge phrases like 'unfortunately' "
            "or 'I know this is disappointing.'"
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Is the task (announcing the cut, preserving morale) and channel context specifically defined?\n"
            "2. Context (0-25): Does it provide the team history, reason for cut, Q1 commitment, and emotional context Copilot needs?\n"
            "3. Source (0-25): Are the key facts (3 weeks of work, 3 engineers, scope reason, Q1 commitment) provided as content for the message?\n"
            "4. Expectations (0-25): Are tone, format, length, required content elements, and prohibited phrases stated?"
        ),
    },

    # ── WORD COPILOT ───────────────────────────────────────────────────────────
    {
        "id": "copilot_word_prd_from_files",
        "category": "word",
        "category_label": "Word Copilot",
        "icon": "📝",
        "title": "Draft a PRD from Reference Files",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "track": "copilot",
        "scenario": (
            "You need to write a Product Requirements Document for a new Customer Self-Service "
            "Portal. You have three source files: a discovery research summary, a technical "
            "architecture proposal from your engineering lead, and a competitive analysis from "
            "the strategy team. Use Word Copilot to synthesize all three into a first-draft PRD "
            "in under 30 minutes."
        ),
        "context": (
            "The portal will let customers manage account settings, view invoices, and submit "
            "support tickets without calling support. Current volume: 1,200 support calls/month, "
            "40% of which are self-servable. Engineering estimate: 8 weeks. Target audience for "
            "the PRD: 3 backend engineers who will implement directly from it with no PM follow-up."
        ),
        "what_makes_a_great_prompt": [
            "Use the `/` slash command in Word Copilot's Draft box to reference source files: type /[filename] and Copilot reads and incorporates it. You can reference up to 10 files in one prompt. Files must be saved in OneDrive or SharePoint — local files won't work. This is the single most powerful Word Copilot feature for document synthesis.",
            "Tell Copilot which source to use for each section: 'Use /[research_summary.docx] for the Problem Statement. Use /[architecture.docx] for Technical Constraints. Use /[competitive_analysis.docx] for Success Metrics.' This explicit attribution produces better synthesis than letting Copilot decide what to pull from where — it tends to over-weight the first file.",
            "Specify the PRD structure as a numbered list of exact section names — don't expect Copilot to know your template: 'Structure: 1) Problem Statement 2) Goals & Success Metrics 3) User Stories 4) Functional Requirements 5) Non-Goals 6) Open Questions.' Named sections reliably produce named sections in the output.",
            "Ask Copilot to flag content gaps explicitly: 'If any required section cannot be completed from the provided files, write [GAP: description]. Do not invent facts not in the source files.' The GAP flag is a work list for what you need to write manually — far more useful than Copilot hallucinating missing content.",
            "Tell Copilot the audience and detail level: 'This PRD goes directly to 3 backend engineers who will implement without further PM involvement. Write functional requirements at implementation level, not feature description level.' This single instruction significantly increases the specificity and usefulness of requirements.",
        ],
        "model_prompt": (
            "Goal: Draft a Product Requirements Document for a Customer Self-Service Portal.\n\n"
            "Sources (use each file for the specified sections):\n"
            "- /[discovery_research.docx] → Problem Statement and user pain points\n"
            "- /[architecture_proposal.docx] → Technical Constraints and assumptions\n"
            "- /[competitive_analysis.docx] → Success Metrics and competitive context\n\n"
            "Context: The portal lets customers manage accounts, view invoices, and submit support "
            "tickets without calling support. Current: 1,200 support calls/month, 40% self-servable. "
            "Engineering estimate: 8 weeks. This PRD goes directly to 3 backend engineers — "
            "no PM follow-up. Write at implementation detail level.\n\n"
            "Structure (use exactly these section names):\n"
            "1. Problem Statement (1 paragraph — use specific pain points from research doc)\n"
            "2. Goals & Success Metrics (bullet list — metrics must have measurable numbers)\n"
            "3. User Stories (3-5 stories in 'As a [user] I want [goal] so that [benefit]' format)\n"
            "4. Functional Requirements (numbered — each requirement implementation-ready, "
            "not feature descriptions)\n"
            "5. Non-Goals (minimum 5 items — explicit out-of-scope)\n"
            "6. Technical Constraints (from architecture doc)\n"
            "7. Open Questions (write [GAP: description] for any missing source material — "
            "do not invent facts)"
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Is the document type, purpose, and scope clearly defined?\n"
            "2. Context (0-25): Does it provide the business situation, user need, engineering context, and audience (backend engineers, implementation level)?\n"
            "3. Source (0-25): Are specific source files referenced using the slash command AND each file assigned to specific sections (the most critical element for this challenge)?\n"
            "4. Expectations (0-25): Is the PRD structure specified, with fidelity rules (no invented facts, GAP flags, implementation-level detail)?"
        ),
    },
    {
        "id": "copilot_word_exec_rewrite",
        "category": "word",
        "category_label": "Word Copilot",
        "icon": "📝",
        "title": "Rewrite a Technical Doc for Executives",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "track": "copilot",
        "scenario": (
            "Your engineering lead wrote an 8-page technical specification for a new event "
            "processing pipeline. You need to present a summary to the executive team next week. "
            "The spec is full of architecture diagrams, Kafka configuration details, and "
            "throughput benchmarks. Use Word Copilot to transform it into a 1-page executive brief."
        ),
        "context": (
            "The spec covers a migration from polling-based to event-driven architecture. "
            "Business case: current polling causes 200ms latency and high DB load; the new "
            "system enables real-time processing and supports 10x current data volume. "
            "Decision required: approve a 3-month engineering investment. "
            "Audience: CEO, CFO, and CPO — none are technical."
        ),
        "what_makes_a_great_prompt": [
            "Use 'Rewrite' not 'Summarize' — the distinction matters. Summarize extracts key points. Rewrite transforms content for a different audience. For audience translation (technical to executive), 'Rewrite for [audience description]' produces dramatically different and better results than 'Summarize for.'",
            "Tell Copilot what executives care about AND what they don't — both sides: 'Executives need: (1) business capability enabled, (2) investment required, (3) risk of not acting. They do NOT need: architecture names, latency benchmarks, or protocol details.' The negative constraint is as important as the positive.",
            "Specify what to DELETE, not just what to add: 'Remove all technology names (Kafka, Kinesis, REST), all latency/throughput numbers, and all architecture details. Replace technical capabilities with business capabilities.' Without explicit deletion instructions, technical content survives the rewrite — Copilot preserves rather than transforms by default.",
            "Constrain the output format strictly: '1 page maximum. Three sections: What This Enables | Investment Required | Risk of Not Acting Now. No paragraphs longer than 3 sentences. Bold key numbers and timeline.' Clear format constraints produce consistently clean output.",
            "Add a jargon self-check: 'After rewriting, flag any remaining technical jargon with [JARGON: word]. I will review before publishing.' This two-step process catches residual terms like API, pipeline, or throughput that survive the rewrite — especially important for a deck going to a CFO.",
        ],
        "model_prompt": (
            "Goal: Rewrite this 8-page technical specification as a 1-page executive brief.\n\n"
            "Audience: CEO, CFO, CPO — none have engineering backgrounds. They need: business "
            "value, investment required, and risk. They do NOT need architecture details.\n\n"
            "Context: The spec is for a migration from polling-based to event-driven data processing. "
            "Business case: current system causes 200ms latency and DB load issues; new system "
            "enables real-time processing at 10x scale. Decision needed: approve 3-month "
            "engineering investment.\n\n"
            "Rewrite rules:\n"
            "- REMOVE: all technology names (Kafka, REST, Kinesis, microservices), all latency/"
            "throughput metrics, all architecture details, code snippets\n"
            "- REPLACE technical capabilities with business capabilities "
            "('processes payments in real time' not 'sub-100ms event processing')\n"
            "- KEEP: business value, timeline in plain weeks/months, what breaks if not built\n\n"
            "Output format: 1 page maximum, 3 sections:\n"
            "1. What This Enables (3 bullet points of business capabilities — no tech jargon)\n"
            "2. Investment Required (timeline, team, costs — plain English numbers only)\n"
            "3. Why Now (risk and cost of delaying this investment)\n\n"
            "After rewriting: flag any remaining technical jargon with [JARGON: word] for my review."
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Is the transformation goal specific — tech spec to exec brief, 1 page, 3 named executives?\n"
            "2. Context (0-25): Does it explain the business case, decision needed, and audience profile?\n"
            "3. Source (0-25): Are specific content deletion rules and the business translation requirement specified (what to remove and what to replace with)?\n"
            "4. Expectations (0-25): Are output format (1 page, 3 sections), tone, length per section, and jargon self-check specified?"
        ),
    },
    {
        "id": "copilot_word_vendor_analysis",
        "category": "word",
        "category_label": "Word Copilot",
        "icon": "📝",
        "title": "Analyze a Vendor Proposal with Q&A",
        "difficulty": "beginner",
        "xp_reward": 50,
        "track": "copilot",
        "scenario": (
            "A vendor sent you a 25-page integration proposal for an analytics platform. "
            "You need to evaluate it against your requirements before a vendor call tomorrow afternoon. "
            "You don't have time to read all 25 pages. Use Word Copilot's Q&A feature to "
            "evaluate it efficiently in under 20 minutes."
        ),
        "context": (
            "Your requirements: API response time <200ms, SOC2 Type II and GDPR compliant, "
            "supports REST API and webhook event triggers, 99.9% uptime SLA. You also need to "
            "identify what the vendor doesn't mention — integration proposals routinely omit "
            "data residency, rate limits, and support escalation paths."
        ),
        "what_makes_a_great_prompt": [
            "Open the vendor document in Word and use the Copilot chat pane for targeted Q&A — don't ask for a generic summary first. Ask your evaluation questions directly. Copilot's answers include citation numbers that link to exact quotes in the document — always use these to verify before your call.",
            "Structure your evaluation as a requirements checklist in the Goal: 'Evaluate against my 5 requirements: [list]. For each: yes/no/partial + quote the exact sentence from the document.' This structured format produces a fast, defensible evaluation rather than a narrative you'd have to re-read.",
            "Ask what's NOT in the proposal: 'What typical enterprise integration requirements are NOT addressed in this document?' Copilot can identify gaps based on standard proposal content — this catches the items vendors strategically omit (rate limits, data residency, escalation paths).",
            "Ask for risk signals in the Source element: 'Flag any commitment that uses hedge language (may, typically, we aim to) instead of contractual language. List them.' Hedge language marks where the vendor is unwilling to commit — these become your negotiation points.",
            "Ask Copilot to prepare your call: 'Based on this proposal and my requirements, what are the 3 most important questions to ask the vendor tomorrow?' 30 seconds of Copilot prep vs. 30 minutes of manual question preparation — this is one of the highest-ROI prompts in this challenge.",
        ],
        "model_prompt": (
            "Goal: Evaluate this 25-page vendor proposal against my requirements before a vendor "
            "call tomorrow afternoon.\n\n"
            "My requirements — assess each explicitly:\n"
            "1. API response time: must be <200ms at p95\n"
            "2. Compliance: SOC2 Type II certified AND GDPR compliant\n"
            "3. Integration: supports REST API and webhook-based event triggers\n"
            "4. SLA: 99.9% uptime guarantee with defined penalties for breach\n"
            "5. Support: named account manager or dedicated support tier\n\n"
            "For each requirement: yes / no / partial + quote the exact sentence from the "
            "document that supports the answer. If not addressed anywhere, write 'not mentioned.'\n\n"
            "After the requirements check:\n"
            "- List 3 typical enterprise integration requirements NOT addressed in this proposal "
            "(data residency, rate limits, escalation paths, etc.)\n"
            "- Flag any commitment using hedge language ('may,' 'typically,' 'we aim to') "
            "instead of contractual commitments — these are negotiation risks\n"
            "- Suggest the 3 most important questions to ask the vendor tomorrow based on the "
            "gaps you found"
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Is the evaluation task defined — requirements checklist, gap analysis, and pre-call prep?\n"
            "2. Context (0-25): Does it state the requirements and the purpose (vendor call tomorrow)?\n"
            "3. Source (0-25): Are the specific requirements Copilot needs to evaluate against provided in enough detail?\n"
            "4. Expectations (0-25): Are the output format (yes/no + quote), gap analysis instructions, hedge-language flag, and question generation all specified?"
        ),
    },
    {
        "id": "copilot_word_notes_to_doc",
        "category": "word",
        "category_label": "Word Copilot",
        "icon": "📝",
        "title": "Transform Workshop Notes into a Strategy Doc",
        "difficulty": "beginner",
        "xp_reward": 50,
        "track": "copilot",
        "scenario": (
            "You just led a 90-minute product strategy workshop with 8 stakeholders. You have "
            "3 pages of raw notes in a Word doc. You need to publish a clean, shareable strategy "
            "document to Confluence before end of day. It's 4pm. Use Word Copilot to transform "
            "your raw notes into a professional document."
        ),
        "context": (
            "Workshop covered: three strategic options for Q4, a decision to pursue option B "
            "(platform consolidation), resource allocation questions that didn't fully resolve, "
            "and a CPO commitment to review the plan next Friday. Four action items were assigned "
            "to different owners. Two open questions remain about budget and headcount."
        ),
        "what_makes_a_great_prompt": [
            "Paste your raw notes into Word first, then use Copilot's Draft feature to generate a structured document below them. Reference the notes content in your Copilot prompt. Having the actual notes in the file dramatically improves output quality compared to describing the notes abstractly.",
            "Tell Copilot the document type in the Goal element: 'Transform these notes into a strategy document' not 'organize my notes.' The document type shapes everything — a strategy document has different sections, tone, and depth than meeting minutes. If you need both, ask Copilot to generate both separately.",
            "Explicitly separate decisions from discussion in the Expectations: 'Clearly separate confirmed decisions from discussion context. Mark anything unconfirmed with [UNCONFIRMED].' Without this instruction, Copilot blends decisions and discussion in a way that misleads readers who weren't in the room.",
            "Specify content fidelity rules in the Source element: 'Keep owner names, dates, and amounts exactly as written in the notes. Add narrative context where it helps readability, but do not invent facts not in the notes.' This two-part rule prevents hallucination while allowing Copilot to add connective tissue.",
            "Ask Copilot to audit its own output: 'After generating the document, list: what information in a complete strategy document is missing from these notes?' This audit produces an explicit to-do list for you before publishing — preventing the embarrassment of publishing an incomplete document.",
        ],
        "model_prompt": (
            "Goal: Transform these raw workshop notes into a 2-page strategy document for "
            "publishing to Confluence today.\n\n"
            "Context: Notes from a 90-minute Q4 product strategy workshop with 8 stakeholders "
            "including the CPO. A major decision was made (option B: platform consolidation). "
            "Some resource questions remain open. The document will be read by 30+ people "
            "who were not in the room.\n\n"
            "Source: Use the raw notes in this document as the only source. Keep all names, "
            "dates, and numbers exactly as written. Add narrative context where helpful — "
            "do not invent facts.\n\n"
            "Structure:\n"
            "1. Executive Summary (3 sentences: what was decided, why, what's next)\n"
            "2. Decision Made (confirmed decision + rationale — mark anything unconfirmed with [UNCONFIRMED])\n"
            "3. Strategic Context (1 paragraph: why option B over other options)\n"
            "4. Action Items (table: Owner | Action — verb-first | Due Date — use names/dates verbatim)\n"
            "5. Open Questions (numbered — items discussed but not resolved)\n"
            "6. Next Steps (what happens before the CPO review next Friday)\n\n"
            "After the document: list what information is missing that a complete strategy doc "
            "would include."
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Is the transformation goal specific — 2-page strategy doc, 6 sections, Confluence-ready, end-of-day deadline?\n"
            "2. Context (0-25): Does it describe the workshop context, decision made, audience (30+ people not in room), and stakes?\n"
            "3. Source (0-25): Are content fidelity rules specified (use notes only, keep names verbatim, don't invent facts)?\n"
            "4. Expectations (0-25): Are all 6 sections defined, the post-generation audit requested, and the [UNCONFIRMED] flag specified?"
        ),
    },

    # ── EXCEL COPILOT ──────────────────────────────────────────────────────────
    {
        "id": "copilot_excel_formula_kpi",
        "category": "excel",
        "category_label": "Excel Copilot",
        "icon": "📊",
        "title": "Build Formula Columns for a KPI Tracker",
        "difficulty": "beginner",
        "xp_reward": 50,
        "track": "copilot",
        "scenario": (
            "You maintain a monthly product KPI spreadsheet with columns for Revenue, Active Users, "
            "New Users, and Churned Users. Your VP wants three calculated metrics added before "
            "tomorrow's review: MoM Revenue Growth %, Churn Rate, and a Risk Flag. "
            "You're not confident in Excel formulas. Use Copilot to build them correctly."
        ),
        "context": (
            "The data is in an Excel Table named 'KPIData' with 12 months of data. "
            "The Risk Flag thresholds your VP specified: RED if Churn Rate > 5% or Revenue Growth < -3%, "
            "YELLOW if Churn Rate 3-5% or Revenue Growth 0 to -3%, GREEN otherwise. "
            "This table is shown in executive presentations — no error cells (#DIV/0!, #REF!) "
            "are acceptable."
        ),
        "what_makes_a_great_prompt": [
            "Ensure your data is in a formatted Excel Table (Insert → Table) before using Copilot. Table headers — not cell references like C2 — are how Copilot identifies columns. 'Create a column using the [Revenue] column' works far more reliably than 'use column C.' Format as a table first; name columns descriptively; Copilot accuracy improves dramatically.",
            "Describe the formula logic in plain English, not in Excel syntax: 'Create a column showing Revenue percentage change compared to the previous month.' Copilot translates your intent to formula — you don't need to know IFERROR, OFFSET, or INDEX. The more naturally you describe the logic, the more accurately Copilot builds it.",
            "Always ask for error handling in the Source element: 'Handle the case where the previous month's Revenue is zero — return N/A instead of a divide-by-zero error.' Error handling is the #1 thing Excel novices miss. Specifying it produces production-ready formulas that won't embarrass you in an executive presentation.",
            "Ask Copilot to explain each formula before applying it: 'Show me what this formula does in one sentence before applying it.' This lets you verify correctness even without knowing Excel — critical for formulas that drive executive decisions about KPIs.",
            "Request formulas in the order they'll be referenced: Churn Rate must be created before the Risk Flag references it. If a formula references a column that doesn't exist yet, Copilot's formula will fail. Order matters — ask for dependent columns after the columns they depend on.",
        ],
        "model_prompt": (
            "Goal: Add 3 calculated columns to my KPI tracker for tomorrow's VP review.\n\n"
            "Context: Excel Table named 'KPIData' with columns: Month, Revenue, Active Users, "
            "New Users, Churned Users. 12 months of data. This table is in executive presentations "
            "— no error cells (#DIV/0!, #REF!) are acceptable under any circumstances.\n\n"
            "Create these columns in order (each depends on the previous):\n\n"
            "1. MoM Revenue Growth %\n"
            "   - Logic: percentage change in Revenue vs. previous month's Revenue\n"
            "   - Error handling: show 'N/A' for row 1 (no prior month); show 'N/A' if previous Revenue is 0\n"
            "   - Format: percentage, 1 decimal place\n\n"
            "2. Churn Rate\n"
            "   - Logic: Churned Users ÷ (Active Users + New Users - Churned Users)\n"
            "   - Error handling: show 'N/A' if denominator is 0\n"
            "   - Format: percentage, 1 decimal place\n\n"
            "3. Risk Flag\n"
            "   - RED: Churn Rate > 5% OR MoM Revenue Growth % < -3%\n"
            "   - YELLOW: Churn Rate 3-5% OR MoM Revenue Growth % between -3% and 0%\n"
            "   - GREEN: all other cases\n\n"
            "For each formula: explain what it does in one sentence before applying it."
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Are the 3 formulas and their business purpose (VP review, executive presentation) clearly defined?\n"
            "2. Context (0-25): Does it specify the table name, column names, and the error-free requirement for executive use?\n"
            "3. Source (0-25): Are the calculation logic, column references, error handling rules, and the dependency order all provided?\n"
            "4. Expectations (0-25): Are number formats, RED/YELLOW/GREEN thresholds, explanation request, and the creation order specified?"
        ),
    },
    {
        "id": "copilot_excel_data_insights",
        "category": "excel",
        "category_label": "Excel Copilot",
        "icon": "📊",
        "title": "Extract Product Insights for a Board Narrative",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "track": "copilot",
        "scenario": (
            "Your Q3 metrics spreadsheet has 6 months of data across 4 product lines "
            "(Consumer, SMB, Enterprise, API). Each row is a monthly snapshot with columns "
            "for Revenue, MAU, Churn Rate, NPS, and Support Tickets. You need 3 board-ready "
            "insight bullets for next week's board meeting. Use Copilot to extract the insights."
        ),
        "context": (
            "You suspect Enterprise is growing fast but generating a disproportionate support load. "
            "Consumer metrics may be declining. NPS seems inversely correlated with Support Ticket "
            "volume in some product lines. The board cares about: growth (Revenue + MAU), "
            "efficiency (revenue per support ticket), and retention (Churn + NPS)."
        ),
        "what_makes_a_great_prompt": [
            "Ask specific analytical questions, not 'analyze my data.' 'What are the top 3 trends over the last 6 months?' produces better analysis than 'tell me about the data.' Vague queries produce vague descriptions. The more specific the question, the more specific and useful the answer.",
            "Ask Copilot to detect anomalies: 'Are there any months where a metric changed by more than 20% vs. the prior month? Flag them: Product Line | Month | Metric | Change.' Anomaly detection is one of Copilot's highest-value Excel capabilities — it finds the signal that manual scrolling would take 30 minutes to spot.",
            "Ask for a derived metric that requires combining columns: 'Calculate Revenue per Support Ticket for each product line and rank them. Highest = most efficient.' This kind of cross-column analysis that Copilot generates instantly would require manual PivotTables and formulas otherwise.",
            "Ask for the board narrative explicitly: 'Write 3 board-ready insight bullets in format: [What's happening] + [which product lines] + [board-level implication]. Write at VP-presenting-to-investors level, not analyst level.' The narrative framing produces board-quality language from raw data — not a data dump.",
            "Ask Copilot to build the visualization: 'What chart type would best show NPS vs. Churn Rate across the 4 product lines over 6 months? Create that chart.' Let Copilot propose and build the visualization — it often makes better choices than the default Insert Chart wizard.",
        ],
        "model_prompt": (
            "Goal: Extract 3 board-ready insights from Q3 product metrics for a board presentation "
            "next week.\n\n"
            "Context: 6-month dataset, 4 product lines (Consumer, SMB, Enterprise, API). "
            "Columns: Product Line, Month, Revenue, MAU, Churn Rate, NPS, Support Tickets. "
            "Board priorities: growth (Revenue + MAU), efficiency (revenue per support ticket), "
            "retention (Churn + NPS). I suspect Enterprise is growing fast but driving high "
            "support load.\n\n"
            "Analysis needed:\n"
            "1. Top 3 trends: what has changed most meaningfully over 6 months? "
            "(product line + metric + direction + magnitude)\n"
            "2. Anomalies: any months where a metric changed >20% vs. prior month? "
            "Flag: Product Line | Month | Metric | % Change\n"
            "3. Efficiency ranking: calculate Revenue per Support Ticket per product line, "
            "rank highest to lowest. Flag the least efficient — what might explain it?\n"
            "4. NPS vs. Churn: is there a visible relationship across product lines? "
            "Describe what you observe.\n"
            "5. Board narrative: write 3 bullet points in format: "
            "[What's happening] + [which product lines] + [board-level implication]. "
            "No analyst language — write as a VP presenting to investors.\n\n"
            "Also: create a chart showing NPS and Churn Rate trends for all 4 product lines "
            "over 6 months."
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Is the analytical objective specific — 3 board bullets, 5 defined analyses, chart?\n"
            "2. Context (0-25): Does it describe the data structure, board's priorities, and the hypothesis to test (Enterprise efficiency)?\n"
            "3. Source (0-25): Are specific column names, product lines, metrics, and analysis types provided to direct Copilot's analysis?\n"
            "4. Expectations (0-25): Is the board narrative format defined, anomaly flag format specified, and visualization requested?"
        ),
    },
    {
        "id": "copilot_excel_conditional_format",
        "category": "excel",
        "category_label": "Excel Copilot",
        "icon": "📊",
        "title": "Make a Roadmap Tracker Scannable",
        "difficulty": "beginner",
        "xp_reward": 50,
        "track": "copilot",
        "scenario": (
            "Your Q4 product roadmap tracker has 35 features with columns for Owner, Due Date, "
            "Priority, Status, and Dependencies. You present this in a 10-minute weekly leadership "
            "review. Right now it's a wall of undifferentiated rows. Use Copilot to apply "
            "conditional formatting that makes risks and status visible at a glance."
        ),
        "context": (
            "Leadership needs to spot overdue items, at-risk work, and ownership gaps without "
            "reading every row. Status values in the sheet: Not Started, In Progress, At Risk, "
            "Blocked, Complete. Some features have blank Owner fields or 'TBD' placeholders that "
            "represent accountability gaps."
        ),
        "what_makes_a_great_prompt": [
            "Describe your formatting rules as business logic, not Excel mechanics: 'Highlight rows where Due Date is in the past AND Status is not Complete' rather than trying to describe the conditional formatting dialog. Copilot translates business intent to precise Excel rules — you don't need to know EDATE, TODAY(), or any formatting syntax.",
            "Prioritize your rules explicitly: 'Apply in this priority order: (1) RED for overdue (2) ORANGE for At Risk/Blocked (3) YELLOW for due within 7 days (4) GREEN for Complete.' When rules could conflict (an overdue item that's now complete), priority order determines which rule wins. Without priority order, results are unpredictable.",
            "Use color + typography combinations for the most critical items: 'RED fill with BOLD text for overdue items.' The combination doubles the visual signal — especially important when the tracker is screenshared in a meeting at low resolution.",
            "Add a data quality rule: 'ORANGE fill on the Owner cell only for rows where Owner is blank, TBD, or Unknown.' Using formatting for data quality flags is a high-value PM use of this feature that catches accountability gaps before they become blockers.",
            "Ask for a summary dashboard row after formatting: 'Add a summary section at the top showing: Total Features | Overdue Count | At Risk/Blocked Count | Due This Week Count | Unowned Count — each as a formula.' This creates a live dashboard header in one request that updates automatically as the tracker changes.",
        ],
        "model_prompt": (
            "Goal: Apply conditional formatting to my Q4 roadmap tracker to make risks and status "
            "instantly visible for a 10-minute weekly leadership review.\n\n"
            "Context: Excel table with 35 features. Columns: Feature Name, Owner, Due Date, "
            "Priority, Status, Dependencies. Status values: Not Started, In Progress, At Risk, "
            "Blocked, Complete. Leadership reads this during a 10-minute meeting — they need to "
            "spot risks without reading every row.\n\n"
            "Formatting rules (apply in this priority order — higher number wins when rules conflict):\n"
            "1. HIGHEST — RED fill + BOLD text: rows where Due Date < today AND Status ≠ 'Complete' (overdue)\n"
            "2. ORANGE fill + BOLD: rows where Status = 'At Risk' OR Status = 'Blocked'\n"
            "3. YELLOW fill: rows where Due Date is within the next 7 days AND Status ≠ 'Complete'\n"
            "4. GREEN fill (light): rows where Status = 'Complete'\n"
            "5. Owner cell only — ORANGE FILL: Owner is blank, 'TBD', or 'Unknown' (accountability gap)\n\n"
            "After formatting:\n"
            "- Add a summary row at the top (outside the table): "
            "Total | Overdue | At Risk/Blocked | Due This Week | Complete | Unowned — "
            "each as a live formula that counts matching rows\n"
            "- Add a legend explaining each color and its meaning"
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Is the formatting purpose (risk-visible, scannable in 10-minute meeting) clearly stated?\n"
            "2. Context (0-25): Does it describe the table structure, Status values, and the leadership meeting use case?\n"
            "3. Source (0-25): Are the column names, Status values, and logic for each rule provided with enough precision for accurate implementation?\n"
            "4. Expectations (0-25): Are all 5 rules, priority order, color/typography combinations, dashboard summary, and legend all specified?"
        ),
    },
    {
        "id": "copilot_excel_pivot_analysis",
        "category": "excel",
        "category_label": "Excel Copilot",
        "icon": "📊",
        "title": "Build a Prioritization Pivot Analysis",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "track": "copilot",
        "scenario": (
            "You have a feature request dataset with 156 rows: Feature Name, Requesting Company, "
            "Requester Revenue ($), Request Date, Product Area, and Priority (voted by requestors). "
            "Leadership is asking which product areas to invest in for Q4. Use Copilot to build "
            "the analysis that makes the case."
        ),
        "context": (
            "You need to distinguish product areas with high demand from high-revenue customers "
            "vs. areas with many requests from small customers. Some product areas have dozens of "
            "requests from SMBs (breadth without value); others have few requests but from "
            "enterprise accounts worth $1M+/year (value without breadth). The decision will "
            "allocate 3 engineering teams for the quarter."
        ),
        "what_makes_a_great_prompt": [
            "State the business question you're answering, not the Excel operation you want: 'I need to know which product areas have the most demand from our highest-revenue customers.' This framing lets Copilot choose the right analysis structure — it produces better results than asking for a specific pivot configuration.",
            "Ask for two parallel analyses to expose the breadth vs. value gap: 'Create two analyses: (1) Request count by product area (2) Total requesting-company revenue by product area. Show both so I can identify areas with high requests but low revenue — and vice versa.' Two views of the same data reveal the gap that one view hides.",
            "Ask for a derived metric that doesn't exist in the data: 'Add a Revenue-per-Request column (Total Revenue ÷ Request Count). Sort by this metric descending. This shows value density, not just volume.' Derived metrics that combine columns are where Copilot adds the most analytical value — they surface insights invisible in raw data.",
            "Ask for a time dimension: 'Add Average Days Since Request Date per product area. High request age + high revenue = most neglected high-value need.' Combining time and revenue identifies frustrated enterprise customers — a signal your data contains but that requires this specific combination to surface.",
            "Ask Copilot to write the recommendation: 'Based on this analysis, which 3 product areas should be Q4 priorities? Write a 1-sentence data-backed rationale per area, citing specific numbers.' Let Copilot do the last-mile interpretation — a recommendation with specific numbers is more persuasive to leadership than your summary without them.",
        ],
        "model_prompt": (
            "Goal: Build an analysis of 156 feature requests to recommend which 3 product areas "
            "to invest in for Q4 — and make the case with data.\n\n"
            "Context: Dataset columns: Feature Name, Requesting Company, Requester Revenue ($), "
            "Request Date, Product Area, Priority (1-5, requestor-voted). Decision: 3 engineering "
            "teams for the quarter. Key distinction to surface: 'high request volume' vs. "
            "'high revenue from requestors' are often different product areas.\n\n"
            "Build this analysis:\n"
            "1. Summary pivot: Product Area | # Requests | Total Requester Revenue | "
            "Revenue-per-Request (Revenue ÷ Requests) | Avg Request Age (days) | "
            "Top Requesting Company — sort by Revenue-per-Request descending. "
            "Highlight top 3 by Revenue-per-Request in green.\n\n"
            "2. Breadth vs. Value gap: identify product areas where Request Count > 20 "
            "but Revenue-per-Request is in the bottom 50% — flag as 'High Volume, Low Value'\n\n"
            "3. Neglected high-value areas: product areas in the top 5 by Revenue AND "
            "Avg Request Age > 180 days — flag as 'High Value, Long Wait'\n\n"
            "4. Q4 recommendation: top 3 product areas to invest in. "
            "For each: 1-sentence rationale citing specific numbers from this analysis. "
            "Flag any area where the data is ambiguous."
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Is the decision to inform (3 product areas for Q4) specifically stated?\n"
            "2. Context (0-25): Does it explain the allocation decision, the breadth vs. value distinction, and team constraint?\n"
            "3. Source (0-25): Are the column names, dataset size, and specific metrics for each analysis component provided?\n"
            "4. Expectations (0-25): Are the pivot structure, derived metrics (Revenue-per-Request), gap analysis logic, and recommendation format specified?"
        ),
    },

    # ── POWERPOINT COPILOT ─────────────────────────────────────────────────────
    {
        "id": "copilot_ppt_from_prd",
        "category": "powerpoint",
        "category_label": "PowerPoint Copilot",
        "icon": "🎨",
        "title": "Create a Deck from a Word PRD",
        "difficulty": "beginner",
        "xp_reward": 50,
        "track": "copilot",
        "scenario": (
            "You just finished writing a 6-page PRD for a new Search feature. Your CPO wants "
            "a 10-minute all-hands presentation by tomorrow morning. You have 40 minutes. "
            "Use Copilot in PowerPoint to convert the PRD into a presentation — faster than "
            "building from scratch."
        ),
        "context": (
            "The PRD covers: problem statement (search is slow and returns irrelevant results), "
            "solution (Elasticsearch-based semantic search), success metrics (search-to-result "
            "<500ms, relevance >85%), timeline (3 sprints), and resource requirements "
            "(2 engineers, 1 design sprint). All-hands audience: 60-person company including "
            "engineering, design, sales, and support."
        ),
        "what_makes_a_great_prompt": [
            "Use 'Create a presentation from file' and reference the PRD using /[filename] — not a text description. This grounds the deck in your actual content rather than Copilot's invention. Type 'Create a presentation based on /[Search_PRD.docx]' — the file must be saved in OneDrive or SharePoint.",
            "Specify the slide count explicitly: 'Create a maximum of 10 slides.' Without this constraint, Copilot generates too many slides — 18 slides for a 10-minute talk doesn't work for any audience. The constraint forces prioritization of what matters most.",
            "Tell Copilot the narrative arc you want, not the PRD section structure: 'Arc: Problem → Business Impact → Solution → Success Metrics → Timeline → What We Need. Do NOT follow the PRD sections — use this story structure.' PRD structure (requirements, non-goals, technical constraints) produces a spec, not a presentation.",
            "Ask for speaker notes on every slide: 'Add speaker notes to every slide with 2-3 sentences of context that don't fit on the slide itself.' Speaker notes are the most overlooked PowerPoint Copilot feature — they're where the real presentation lives, and they save you from reading your own slides.",
            "After generating, ask Copilot to identify what to cut: 'Which 2 slides could be removed without losing the core message?' This editing question is a second pass that often reveals redundant slides — and it's much easier than deciding what to cut yourself after generating a full deck.",
        ],
        "model_prompt": (
            "Goal: Create a 10-slide maximum all-hands presentation for a 10-minute talk based "
            "on /[Search_Feature_PRD.docx].\n\n"
            "Context: Audience is 60 people across engineering, design, sales, support — all "
            "company levels, not just PMs. This is an all-hands announcement, not a spec review. "
            "People need to understand what we're building and why — not the technical details.\n\n"
            "Narrative arc (use this, NOT the PRD's section structure):\n"
            "1. The Problem (why search is broken today — use specific pain from PRD — 1 slide)\n"
            "2. Business Impact (what this costs us — 1 slide)\n"
            "3. The Solution (what we're building in plain English — 2 slides max)\n"
            "4. How We'll Know It Works (success metrics — 1 slide)\n"
            "5. Timeline (milestones — 1 slide)\n"
            "6. What We Need (resources and asks — 1 slide)\n\n"
            "Requirements:\n"
            "- Maximum 10 slides total\n"
            "- Max 5 bullet points per slide — no text walls\n"
            "- Add speaker notes to every slide (2-3 sentences of context per slide)\n"
            "- Plain English only: no technical jargon (no Elasticsearch, p95, semantic vector)\n"
            "- After generating: which 2 slides are least essential and could be cut?"
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Is the presentation type (all-hands, 10 minutes), slide limit, and purpose defined?\n"
            "2. Context (0-25): Does it describe the audience (60-person all-hands), the tone (announcement vs. review), and the business context?\n"
            "3. Source (0-25): Is the PRD referenced via the slash command (the key feature for this challenge type)?\n"
            "4. Expectations (0-25): Is the narrative arc specified (not PRD structure), speaker notes requested, jargon prohibited, and post-generation editing question included?"
        ),
    },
    {
        "id": "copilot_ppt_speaker_notes",
        "category": "powerpoint",
        "category_label": "PowerPoint Copilot",
        "icon": "🎨",
        "title": "Add Speaker Notes to an Existing Deck",
        "difficulty": "beginner",
        "xp_reward": 50,
        "track": "copilot",
        "scenario": (
            "Your team built a 16-slide QBR deck over two weeks. You're presenting it to senior "
            "leadership tomorrow at 9am and you haven't internalized all the content. It's 7pm. "
            "Use Copilot to add speaker notes that will help you present each slide confidently "
            "without reading from it."
        ),
        "context": (
            "The QBR covers Q3 performance (revenue, MAU growth, churn, NPS), product milestones, "
            "competitive win/loss analysis, Q4 roadmap priorities, and resource requests. "
            "Most slides have bullet points only — no narrative. Senior leadership expects the "
            "story behind the data. You have roughly 4 minutes per slide for a 60-minute deck."
        ),
        "what_makes_a_great_prompt": [
            "'Add speaker notes to all slides' is a single Copilot command that populates the entire deck at once — this is one of PowerPoint Copilot's most powerful features. But generic notes ('This slide covers Q3 revenue performance') aren't useful. Give Copilot specific instructions about what the notes should contain.",
            "Specify time constraint per slide in the Expectations: 'Each slide has approximately 4 minutes. Speaker notes should cover only the 1-2 most important things to say — not everything on the slide. Add context that isn't visible, not a narration of the bullets.' This produces notes that guide your talk rather than script recitation.",
            "Ask for 'the story behind the data' explicitly: 'For every data slide, speaker notes must explain: why is this result good or bad? what caused it? what should the audience take away?' This is the difference between a presenter who reads numbers and one who interprets them — exactly what senior leadership expects.",
            "Ask for transition sentences: 'End every slide's speaker notes with one sentence that transitions to the next slide.' Transitions separate polished presentations from slide-reading — Copilot adds them across all 16 slides in one pass, saving you 30 minutes of writing.",
            "Ask for anticipated questions: 'After adding notes to all slides, identify the 3 slides most likely to generate tough questions from senior leadership and suggest a likely question + recommended answer for each.' This prep normally takes 30 anxious minutes — Copilot does it in 30 seconds.",
        ],
        "model_prompt": (
            "Goal: Add speaker notes to all 16 slides of this QBR deck to help me present "
            "confidently tomorrow at 9am without reading from the slides.\n\n"
            "Context: I'm presenting to senior leadership. 60-minute deck = 4 minutes per slide. "
            "Leadership expects the story behind the data, not recitation of bullets. I'm not "
            "fully familiar with all slides — I need notes that guide me, not script me.\n\n"
            "For every slide, speaker notes must include:\n"
            "1. The 1-2 most important points to make (4-minute constraint — don't cover everything)\n"
            "2. Context not on the slide: why does this number matter? What caused it? "
            "What should leadership take away?\n"
            "3. A transition sentence at the end leading into the next slide\n"
            "4. For any metric slide: one sentence starting with 'Why this matters:' — "
            "the business implication, not just the number\n\n"
            "After adding notes to all slides:\n"
            "- Identify the 3 slides most likely to generate challenging questions from "
            "senior leadership\n"
            "- For each: the likely question AND a recommended answer (2-3 sentences)\n"
            "- Flag any slide where the data seems incomplete or challengeable with ⚠️"
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Is the purpose (guide my talk, 16 slides, 9am deadline) specifically defined?\n"
            "2. Context (0-25): Does it describe the time constraint (4 min/slide), audience (senior leadership), presentation type (QBR), and presenter's situation?\n"
            "3. Source (0-25): Does it reference the specific deck and the time parameters Copilot needs to calibrate note length and scope?\n"
            "4. Expectations (0-25): Are the 4 note components, transition requirement, 'Why this matters' instruction, and post-generation prep analysis all specified?"
        ),
    },
    {
        "id": "copilot_ppt_restructure",
        "category": "powerpoint",
        "category_label": "PowerPoint Copilot",
        "icon": "🎨",
        "title": "Diagnose and Restructure a Partnership Deck",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "track": "copilot",
        "scenario": (
            "You have a 22-slide partnership proposal deck built by 3 different team members "
            "over 2 months. The story is fragmented, the slide order is confusing, and there is "
            "no clear ask at the end. A high-stakes partnership meeting is in 48 hours. "
            "Use Copilot to diagnose the problems and restructure the deck."
        ),
        "context": (
            "The deck covers company background (7 slides), proposed partnership structure (4 slides), "
            "market opportunity (6 slides), and a vague 'next steps' section (5 slides). "
            "Three writing styles make it feel inconsistent. The actual ask is buried in slide 19. "
            "Decision-maker: the target partner's VP of Partnerships. 30-minute meeting."
        ),
        "what_makes_a_great_prompt": [
            "Start with diagnosis before restructuring — this is the most important sequencing insight for this challenge: 'Review this deck and tell me: what's the core message, where does the narrative lose coherence, and what appears to be the ask?' Starting with diagnosis lets you validate Copilot's understanding before it makes changes you'd need to undo.",
            "Ask for the restructuring plan as a numbered slide list BEFORE executing: 'Propose a new slide order as a numbered list of slide titles. Show me the plan before making any changes.' Review and approve — don't let Copilot restructure blindly. This 2-step process prevents losing your starting point.",
            "Ask Copilot to identify slides for the appendix: 'Which slides contain background context that the decision-maker doesn't need in the main deck? Suggest moving them to an appendix.' 22 slides is too many for a 30-minute meeting — Copilot identifying appendix material gets you to 12-14 main slides.",
            "Ask for an executive summary slide: 'Add an executive summary slide as slide 1, maximum 5 bullets. A decision-maker who only reads slide 1 should understand: what we're proposing, the value to them, what we're asking for, and the timeline.' This one slide dramatically improves the odds a time-pressured executive understands your proposal.",
            "Ask for a clear Ask slide: 'Add a dedicated Ask slide at the end: what we want from this partner, what we commit to in return, the timeline we're proposing, and the single next step.' Proposals without a clear ask don't get yes or no — they get 'let's keep the conversation going.' That's a slow no.",
        ],
        "model_prompt": (
            "Goal: Diagnose and restructure this 22-slide partnership proposal for a 30-minute "
            "meeting with the VP of Partnerships in 48 hours.\n\n"
            "Context: Built by 3 people over 2 months — fragmented narrative, inconsistent tone, "
            "the actual ask is buried in slide 19. Decision-maker is a VP of Partnerships who "
            "will have 30 minutes. We need to make an immediate strong impression.\n\n"
            "Step 1 — Diagnose only (do not change anything yet):\n"
            "- Core message of this deck in one sentence\n"
            "- Where does the narrative lose coherence? (specific slides)\n"
            "- Is the intended ask clear? Where is it? Is it specific enough?\n"
            "- Which slides are redundant or overlap each other?\n"
            "- Which slides should move to an appendix (background context, not decision content)?\n\n"
            "Step 2 — Propose restructuring (before executing):\n"
            "- New slide order as a numbered list of slide titles\n"
            "- Slides to move to appendix\n"
            "- Missing slides (executive summary? clear ask?)\n\n"
            "Step 3 — Execute after my approval of Steps 1-2:\n"
            "- Add executive summary as slide 1 (5 bullets max: proposal, value to them, ask, timeline, next step)\n"
            "- Add 'Our Ask' as final slide: what we want | what we commit to | timeline | single next step\n"
            "- Standardize tone: professional, direct, partner-centric (written for their VP, not our team)"
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal Clarity (0-25): Is the task clearly sequenced — diagnose then plan then execute, 48-hour deadline?\n"
            "2. Context (0-25): Does it describe the deck's current problems, the high-stakes meeting, and the decision-maker profile?\n"
            "3. Source (0-25): Does the prompt reference the specific deck and provide enough structural context for meaningful diagnosis?\n"
            "4. Expectations (0-25): Is the 3-step process defined, executive summary and Ask slide requirements specified, and tone standardization included?"
        ),
    },
    {
        "id": "copilot_ppt_framework_mastery",
        "category": "powerpoint",
        "category_label": "PowerPoint Copilot",
        "icon": "🎨",
        "title": "Master Microsoft's 4-Part Prompting Framework",
        "difficulty": "intermediate",
        "xp_reward": 75,
        "track": "copilot",
        "scenario": (
            "You've been using M365 Copilot for 3 weeks and getting mediocre results. A colleague "
            "in the same role gets dramatically better output from the same tools. You discover "
            "the difference: Microsoft's 4-part prompting framework. This challenge tests your "
            "ability to transform a weak prompt into an excellent one using all four elements: "
            "Goal, Context, Source, and Expectations."
        ),
        "context": (
            "Microsoft's official framework for effective Copilot prompts has four required elements: "
            "(1) Goal — what you want Copilot to produce. (2) Context — business situation, "
            "audience, and background. (3) Source — which files, meetings, emails, or data to use. "
            "(4) Expectations — format, length, tone, and audience. Most users only provide Goal. "
            "Adding the other three elements consistently produces significantly better output."
        ),
        "what_makes_a_great_prompt": [
            "The Goal element must specify the OUTPUT TYPE, not just the task: 'Draft a 3-paragraph email with a subject line' is better than 'draft an email.' Output type (email, bullet list, table, 1-page brief, presentation) dramatically narrows what Copilot produces. Add the output type to every prompt you write.",
            "The Context element is the most-skipped and produces the biggest single improvement: 'Draft an email about the project delay' (no context) vs. 'Draft an email about the project delay — root cause was a vendor API incompatibility, not our team's failure, and we have a partial mitigation starting next week.' The second produces a draft that sounds like you wrote it.",
            "The Source element is what makes Copilot different from generic AI tools — it unlocks your organizational data. Use /[filename] in Word and PowerPoint, reference meeting names in Teams Copilot, specify 'based on my emails from the last 7 days' in Outlook Chat. Grounded responses are almost always better than ungrounded ones.",
            "The Expectations element drives format quality: if unspecified, Copilot defaults to a generic format. Three dimensions matter most: structure ('3 bullet points'), length ('under 100 words'), and audience ('written for a non-technical VP'). All three together produce usable output on the first try.",
            "The most common weak-prompt pattern is Goal-only: 'Summarize this meeting' or 'Write a status update.' The fix: after writing every prompt, check — does it have all 4 elements? If any is missing, add it. This one habit produces consistently better results than any individual technique.",
        ],
        "model_prompt": (
            "WEAK PROMPT (Goal only):\n"
            "'Write a project status update for leadership.'\n\n"
            "STRONG PROMPT — all 4 elements of Microsoft's framework:\n\n"
            "GOAL: Write a 1-page weekly project status update for the Q4 Mobile Launch project.\n\n"
            "CONTEXT: We are in week 8 of 12. Phase 1 (MVP features) is 95% complete and on "
            "track. Phase 2 (performance optimization) is 3 days behind due to a critical "
            "payment flow bug discovered Monday. The VP of Product already knows about the bug "
            "— this update acknowledges it, not announces it. No one is being blamed.\n\n"
            "SOURCE: Based on /[Q4_Mobile_Status_Deck.pptx] and the engineering standup notes "
            "from this week in Teams.\n\n"
            "EXPECTATIONS:\n"
            "- Audience: VP of Product and CPO — executives, 3-minute maximum read\n"
            "- Format: (1) Overall status with traffic light GREEN/AMBER/RED, "
            "(2) Phase progress table, (3) Risks with mitigations, (4) Decisions needed this week\n"
            "- Tone: direct and solution-focused — not defensive about the bug, "
            "focused on what we're doing about it\n"
            "- Length: under 400 words\n"
            "- If a leadership decision is needed, phrase it as a yes/no question with a deadline"
        ),
        "evaluation_rubric": (
            "Score this Copilot prompt using Microsoft's 4-part framework (0-25 each):\n"
            "1. Goal (0-25): Is the output type (1-page status update), specific project, and deliverable precisely stated?\n"
            "2. Context (0-25): Is the business situation, phase status, prior knowledge of the issue, and sensitive context richly provided?\n"
            "3. Source (0-25): Are specific organizational data sources (named files, meeting notes) cited using the slash-command pattern?\n"
            "4. Expectations (0-25): Are format structure (4 sections), length, tone, audience, and the decision-question format all explicitly defined?"
        ),
    },
]

COPILOT_CATEGORIES = {
    "outlook":     {"label": "Outlook Copilot",     "icon": "📧", "color": "#0078D4"},
    "teams":       {"label": "Teams Copilot",       "icon": "💬", "color": "#6264A7"},
    "word":        {"label": "Word Copilot",        "icon": "📝", "color": "#185ABD"},
    "excel":       {"label": "Excel Copilot",       "icon": "📊", "color": "#107C41"},
    "powerpoint":  {"label": "PowerPoint Copilot",  "icon": "🎨", "color": "#C43E1C"},
}

COPILOT_BADGES = {
    "copilot_first_challenge": {
        "id": "copilot_first_challenge",
        "name": "Copilot First Steps",
        "description": "Completed your first Copilot challenge",
        "icon": "🚀",
    },
    "copilot_outlook_master": {
        "id": "copilot_outlook_master",
        "name": "Inbox Zero Hero",
        "description": "Completed all Outlook Copilot challenges",
        "icon": "📧",
    },
    "copilot_teams_navigator": {
        "id": "copilot_teams_navigator",
        "name": "Teams Navigator",
        "description": "Completed all Teams Copilot challenges",
        "icon": "💬",
    },
    "copilot_word_master": {
        "id": "copilot_word_master",
        "name": "Word Wizard",
        "description": "Completed all Word Copilot challenges",
        "icon": "📝",
    },
    "copilot_excel_analyst": {
        "id": "copilot_excel_analyst",
        "name": "Excel Analyst",
        "description": "Completed all Excel Copilot challenges",
        "icon": "📊",
    },
    "copilot_ppt_presenter": {
        "id": "copilot_ppt_presenter",
        "name": "Deck Master",
        "description": "Completed all PowerPoint Copilot challenges",
        "icon": "🎨",
    },
    "copilot_framework_expert": {
        "id": "copilot_framework_expert",
        "name": "Framework Expert",
        "description": "Scored 90+ on the 4-Part Framework Mastery challenge",
        "icon": "🧠",
    },
    "copilot_perfectionist": {
        "id": "copilot_perfectionist",
        "name": "Copilot Perfectionist",
        "description": "Scored 95 or higher on any Copilot challenge",
        "icon": "💎",
    },
    "copilot_high_achiever": {
        "id": "copilot_high_achiever",
        "name": "Copilot High Achiever",
        "description": "Scored 80+ on 5 different Copilot challenges",
        "icon": "⭐",
    },
    "copilot_completionist": {
        "id": "copilot_completionist",
        "name": "Copilot Champion",
        "description": "Completed all 20 Copilot challenges",
        "icon": "🏆",
    },
}
