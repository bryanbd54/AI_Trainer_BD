const App = (() => {
  let state = {
    username: null,
    user: null,
    challenges: [],
    categories: {},
    badges: {},
    currentChallenge: null,
    currentTrack: 'copilot',
    challengeTips: [],
    hintsUsed: 0,
  };

  let _adminUsers = [];

  // ── Claude thinking words (106) ───────────────────────────────────────────
  const THINKING_WORDS = [
    'beaming','booping','bouncing','brewing','bubbling','chasing','churning',
    'coalescing','conjuring','cooking','crafting','crunching','cuddling','dancing',
    'dazzling','discovering','doodling','dreaming','drifting','enchanting','exploring',
    'finding','floating','fluttering','foraging','forging','frolicking','gathering',
    'giggling','gliding','greeting','growing','hatching','herding','honking',
    'hopping','hugging','humming','imagining','inventing','jingling','juggling',
    'jumping','kindling','knitting','launching','leaping','mapping','marinating',
    'meandering','mixing','moseying','munching','napping','nibbling','noodling',
    'orbiting','painting','percolating','petting','plotting','pondering','popping',
    'prancing','purring','puzzling','questing','riding','roaming','rolling',
    'sauteeing','scribbling','seeking','shimmying','singing','skipping','sleeping',
    'snacking','sniffing','snuggling','soaring','sparking','spinning','splashing',
    'sprouting','squishing','stargazing','stirring','strolling','swimming','swinging',
    'tickling','tinkering','toasting','tumbling','twirling','waddling','wandering',
    'watching','weaving','whistling','wibbling','wiggling','wishing','wobbling',
    'wondering','yawning','zooming',
  ];

  let _thinkInterval = null;

  function _startThinkingWords() {
    const el = document.getElementById('thinkingWord');
    if (!el) return;
    let i = Math.floor(Math.random() * THINKING_WORDS.length);
    el.textContent = THINKING_WORDS[i];
    _thinkInterval = setInterval(() => {
      i = Math.floor(Math.random() * THINKING_WORDS.length);
      el.textContent = THINKING_WORDS[i];
    }, 2000);
  }

  function _stopThinkingWords() {
    clearInterval(_thinkInterval);
    _thinkInterval = null;
  }

  // ── Track config ──────────────────────────────────────────────────────────

  const TRACK_CONFIG = {
    claude: {
      logo: '🤖 Claude Trainer',
      loadingTitle: 'Claude is evaluating…',
      loadingSubtitle: 'Sending your prompt, generating a response, and scoring your technique.',
      promptTitle: '✍️ Write your prompt for Claude',
      promptDesc: 'Write the prompt you\'d give Claude to complete this task. The better your prompt, the higher your score. Claude will evaluate both your prompt quality and the output it generates.',
      promptPlaceholder: 'Write your prompt here...\nTry to: give Claude a role, provide context, specify the exact format you need...',
      scoreSubtitle: 'Based on Clarity, Context, Structure, and Output Quality',
      responseLabel: '📄 Claude\'s Response to Your Prompt',
      badgesSubtitle: 'Unlock achievements as you master Claude',
      breakdown: { clarity: 'Clarity', context: 'Context', structure: 'Structure', output_quality: 'Output Quality' },
    },
    copilot: {
      logo: '💼 Copilot Trainer',
      loadingTitle: 'Evaluating your Copilot prompt…',
      loadingSubtitle: 'Simulating Copilot\'s response and scoring against Microsoft\'s 4-part framework.',
      promptTitle: '✍️ Write your prompt for M365 Copilot',
      promptDesc: 'Write the prompt you\'d give Microsoft 365 Copilot to complete this task. The better your prompt, the higher your score. Use the Goal → Context → Source → Expectations framework.',
      promptPlaceholder: 'Write your Copilot prompt here...\nTry to: state your Goal, add Context, reference a Source file (/[filename]), specify Expectations...',
      scoreSubtitle: 'Based on Goal, Context, Source, and Expectations',
      responseLabel: '📄 Copilot\'s Simulated Response',
      badgesSubtitle: 'Unlock achievements as you master M365 Copilot',
      breakdown: { clarity: 'Goal', context: 'Context', structure: 'Source', output_quality: 'Expectations' },
    },
  };

  // ── Boot ──────────────────────────────────────────────────────────────────

  async function init() {
    try {
      const status = await api('/api/status');
      if (status.demo_mode) {
        document.getElementById('demoBanner').style.display = 'block';
      }
    } catch (_) {}

    const saved = localStorage.getItem('ct_username');
    if (saved) {
      try {
        const user = await api('/api/users/' + encodeURIComponent(saved));
        state.username = saved;
        state.user = user;
        state.currentTrack = 'copilot';
        await loadChallenges();
        showNav();
        showView('dashboard');
        return;
      } catch (_) {
        localStorage.removeItem('ct_username');
      }
    }
    showView('login');
    document.getElementById('usernameInput').focus();
  }

  async function login() {
    showFormError('loginError', '');
    const username = document.getElementById('usernameInput').value.trim().toLowerCase();
    const password = document.getElementById('passwordInput').value;
    if (!username) { document.getElementById('usernameInput').focus(); return; }
    if (!password) { document.getElementById('passwordInput').focus(); return; }
    try {
      const user = await api('/api/users', 'POST', { username, password });
      state.username = username;
      state.user = user;
      state.currentTrack = 'copilot';
      localStorage.setItem('ct_username', username);
      await loadChallenges();
      showNav();
      renderDashboard();
      showView('dashboard');
    } catch (e) {
      showFormError('loginError', e.message);
    }
  }

  async function register() {
    showFormError('registerError', '');
    const displayName = document.getElementById('regDisplayName').value.trim();
    const username = document.getElementById('regUsername').value.trim().toLowerCase();
    const email = document.getElementById('regEmail').value.trim();
    const password = document.getElementById('regPassword').value;
    const confirm = document.getElementById('regPasswordConfirm').value;

    if (!username) { document.getElementById('regUsername').focus(); return; }
    if (!email || !email.includes('@')) {
      showFormError('registerError', 'Please enter a valid email address.');
      document.getElementById('regEmail').focus();
      return;
    }
    if (password.length < 6) {
      showFormError('registerError', 'Password must be at least 6 characters.');
      document.getElementById('regPassword').focus();
      return;
    }
    if (password !== confirm) {
      showFormError('registerError', 'Passwords do not match.');
      document.getElementById('regPasswordConfirm').focus();
      return;
    }

    try {
      await api('/api/register', 'POST', { username, email, password, display_name: displayName || username });
      document.getElementById('regDisplayName').value = '';
      document.getElementById('regUsername').value = '';
      document.getElementById('regEmail').value = '';
      document.getElementById('regPassword').value = '';
      document.getElementById('regPasswordConfirm').value = '';
      // Auto-login after successful registration
      const user = await api('/api/users', 'POST', { username, password });
      state.username = username;
      state.user = user;
      state.currentTrack = 'copilot';
      localStorage.setItem('ct_username', username);
      await loadChallenges();
      showNav();
      renderDashboard();
      showView('dashboard');
    } catch (e) {
      showFormError('registerError', e.message);
    }
  }

  function logout() {
    localStorage.removeItem('ct_username');
    state.username = null;
    state.user = null;
    state.challenges = [];
    state.categories = {};
    state.badges = {};
    state.currentChallenge = null;
    state.currentTrack = 'copilot';
    document.getElementById('nav').style.display = 'none';
    document.getElementById('usernameInput').value = '';
    document.getElementById('passwordInput').value = '';
    showView('login');
    document.getElementById('usernameInput').focus();
  }

  // ── Track switching ───────────────────────────────────────────────────────

  async function switchTrack(track) {
    if (state.currentTrack === track) return;
    if (track === 'claude' && !state.user?.claude_access) {
      alert('Claude track is locked. Contact your admin to get access.');
      return;
    }
    state.currentTrack = track;
    _applyTrackUI();
    await loadChallenges();
    showView('dashboard');
  }

  function _applyTrackUI() {
    const cfg = TRACK_CONFIG[state.currentTrack];
    document.getElementById('navLogoText').textContent = cfg.logo;
    const claudeBtn = document.getElementById('trackBtnClaude');
    if (claudeBtn) {
      const hasAccess = !!state.user?.claude_access;
      claudeBtn.style.display = hasAccess ? '' : 'none';
      claudeBtn.classList.toggle('active', state.currentTrack === 'claude');
    }
    document.getElementById('trackBtnCopilot').classList.toggle('active', state.currentTrack === 'copilot');
    document.getElementById('loadingTitle').textContent = cfg.loadingTitle;
    document.getElementById('loadingSubtitle').textContent = cfg.loadingSubtitle;
    document.getElementById('promptSectionTitle').textContent = cfg.promptTitle;
    document.getElementById('promptDescription').textContent = cfg.promptDesc;
    document.getElementById('promptInput').placeholder = cfg.promptPlaceholder;
    document.getElementById('responseLabel').textContent = cfg.responseLabel;
    document.getElementById('badgesSubtitle').textContent = cfg.badgesSubtitle;
    _applyBreakdownLabels();
  }

  function _applyBreakdownLabels() {
    const labels = TRACK_CONFIG[state.currentTrack].breakdown;
    document.getElementById('bClarityLabel').textContent = labels.clarity;
    document.getElementById('bContextLabel').textContent = labels.context;
    document.getElementById('bStructureLabel').textContent = labels.structure;
    document.getElementById('bOutputLabel').textContent = labels.output_quality;
  }

  // ── Data ──────────────────────────────────────────────────────────────────

  async function loadChallenges() {
    const data = await api('/api/challenges?track=' + state.currentTrack);
    state.challenges = data.challenges;
    state.categories = data.categories;
    const badgeData = await api('/api/badges?track=' + state.currentTrack);
    state.badges = badgeData;
  }

  async function refreshUser() {
    state.user = await api('/api/users/' + encodeURIComponent(state.username));
    updateNav();
  }

  // ── Views ─────────────────────────────────────────────────────────────────

  function showView(name) {
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    const el = document.getElementById('view-' + name);
    if (el) el.classList.add('active');

    showFormError('loginError', '');
    showFormError('registerError', '');

    if (name === 'dashboard') renderDashboard();
    else if (name === 'leaderboard') renderLeaderboard();
    else if (name === 'badges') renderBadges();
    else if (name === 'admin') loadAdminUsers();
  }

  // ── Nav ───────────────────────────────────────────────────────────────────

  function showNav() {
    document.getElementById('nav').style.display = 'flex';
    _applyTrackUI();
    updateNav();
    const adminBtn = document.getElementById('adminNavBtn');
    if (adminBtn) adminBtn.style.display = state.user?.is_admin ? '' : 'none';
  }

  function updateNav() {
    if (!state.user) return;
    document.getElementById('navUsername').textContent = state.user.display_name || state.user.username;
    document.getElementById('navXp').textContent = state.user.xp + ' XP';
  }

  // ── Dashboard ─────────────────────────────────────────────────────────────

  function renderDashboard() {
    if (!state.user) return;
    const u = state.user;

    document.getElementById('dashWelcome').textContent = 'Hey, ' + (u.display_name || u.username) + '! 👋';
    const comp = Object.keys(u.completions).length;
    const total = state.challenges.length;
    document.getElementById('dashSubtitle').textContent =
      comp === 0
        ? 'Pick your first challenge and start prompting.'
        : `You've completed ${comp} of ${total} challenges. Keep going!`;

    // Level card
    document.getElementById('levelName').textContent = u.level_name;
    document.getElementById('levelXp').textContent = u.xp + ' XP total';
    const li = document.getElementById('levelIcon');
    li.textContent = u.level;
    li.style.background = u.level_color;
    document.getElementById('xpBarFill').style.width = u.progress_pct + '%';
    document.getElementById('xpLabel').textContent = u.xp_to_next > 0
      ? u.xp_to_next + ' XP to next level' : 'Max level reached!';

    // Stats
    document.getElementById('statXp').textContent = u.xp;
    document.getElementById('statCompleted').textContent = comp;
    document.getElementById('statBadges').textContent = u.badges.length;

    const scores = Object.values(u.completions);
    const avg = scores.length ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : null;
    document.getElementById('statAvg').textContent = avg !== null ? avg : '—';

    // Group challenges by category
    const byCategory = {};
    for (const c of state.challenges) {
      if (!byCategory[c.category]) byCategory[c.category] = [];
      byCategory[c.category].push(c);
    }

    const container = document.getElementById('challengeCategories');
    container.innerHTML = '';
    for (const [catId, challenges] of Object.entries(byCategory)) {
      const catInfo = state.categories[catId] || { label: catId, icon: '📌', color: '#7c6cfc' };
      const done = challenges.filter(c => u.completions[c.id] !== undefined).length;

      const section = document.createElement('div');
      section.className = 'category-section';
      section.innerHTML = `
        <div class="category-header">
          <div class="category-dot" style="background:${catInfo.color}"></div>
          <span style="font-size:1.1rem">${catInfo.icon}</span>
          <h2>${catInfo.label}</h2>
          <span class="category-count">${done}/${challenges.length} complete</span>
        </div>
        <div class="challenges-grid" id="grid-${catId}"></div>
      `;
      container.appendChild(section);

      const grid = section.querySelector(`#grid-${catId}`);
      for (const c of challenges) {
        const bestScore = u.completions[c.id];
        const isCompleted = bestScore !== undefined;
        const card = document.createElement('div');
        card.className = 'challenge-card' + (isCompleted ? ' completed' : '');
        card.onclick = () => openChallenge(c.id);
        card.innerHTML = `
          <div class="card-header">
            <span class="card-icon">${c.icon}</span>
            <span class="card-title">${c.title}</span>
            <span class="card-badge badge-${c.difficulty}">${c.difficulty}</span>
          </div>
          <div class="card-scenario">${c.scenario}</div>
          <div class="card-footer">
            <span class="card-xp">⭐ up to ${Math.round(c.xp_reward * 1.5)} XP</span>
            ${isCompleted
              ? `<span class="card-score">✓ Best: ${bestScore}</span>`
              : '<span style="font-size:0.8rem;color:var(--text-muted)">Not started</span>'
            }
          </div>
        `;
        grid.appendChild(card);
      }
    }

    updateNav();
  }

  // ── Challenge Detail ───────────────────────────────────────────────────────

  async function openChallenge(id) {
    let challenge = state.challenges.find(c => c.id === id);
    if (!challenge) return;

    try {
      challenge = await api('/api/challenges/' + id);
    } catch (_) {}

    state.currentChallenge = challenge;
    state.challengeTips = challenge.what_makes_a_great_prompt || [];
    state.hintsUsed = 0;

    document.getElementById('detailCategory').textContent = challenge.category_label;
    document.getElementById('detailDifficulty').textContent = challenge.difficulty;
    document.getElementById('detailXp').textContent = challenge.xp_reward;
    document.getElementById('detailTitle').textContent = challenge.icon + ' ' + challenge.title;
    document.getElementById('detailScenario').textContent = challenge.scenario;
    document.getElementById('detailContext').textContent = challenge.context || '';

    const hintsList = document.getElementById('hintsList');
    const hintsNote = document.getElementById('hintsNote');
    const hintBtn = document.getElementById('hintBtn');
    if (hintsList) hintsList.innerHTML = '';
    if (hintsNote) { hintsNote.style.display = 'none'; hintsNote.textContent = ''; }
    if (hintBtn) { hintBtn.style.display = ''; hintBtn.disabled = false; }

    document.getElementById('promptInput').value = '';
    document.getElementById('charCount').textContent = '0 characters';
    hideResults();

    // Apply track-specific UI for the challenge view
    _applyTrackUI();

    showView('challenge');
    window.scrollTo(0, 0);
  }

  function updateCharCount() {
    const len = document.getElementById('promptInput').value.length;
    document.getElementById('charCount').textContent = len + ' characters';
  }

  function revealHint() {
    const tips = state.challengeTips;
    if (state.hintsUsed >= tips.length) return;

    const hintsList = document.getElementById('hintsList');
    const note = document.getElementById('hintsNote');
    const hintBtn = document.getElementById('hintBtn');
    if (!hintsList) return;

    const li = document.createElement('li');
    li.textContent = tips[state.hintsUsed];
    hintsList.appendChild(li);
    state.hintsUsed++;

    const penalty = state.hintsUsed * 8;
    if (note) {
      note.style.display = 'block';
      note.textContent = state.hintsUsed + ' hint' + (state.hintsUsed > 1 ? 's' : '') +
        ' used — max XP reduced by ' + penalty;
    }

    if (state.hintsUsed >= tips.length && hintBtn) {
      hintBtn.style.display = 'none';
    }
  }

  // ── Submit ────────────────────────────────────────────────────────────────

  async function submitChallenge() {
    const prompt = document.getElementById('promptInput').value.trim();
    if (!prompt) {
      document.getElementById('promptInput').focus();
      return;
    }
    if (!state.currentChallenge) return;

    document.getElementById('submitBtn').disabled = true;
    document.getElementById('loadingOverlay').classList.add('active');
    _startThinkingWords();
    hideResults();

    try {
      const result = await api(
        '/api/challenges/' + state.currentChallenge.id + '/submit',
        'POST',
        { username: state.username, prompt, hints_used: state.hintsUsed }
      );

      state.user = result.user;
      updateNav();
      renderResults(result);

      if (result.new_badges && result.new_badges.length > 0) {
        showBadgeToasts(result.new_badges);
      }
    } catch (e) {
      alert('Submission error: ' + e.message);
    } finally {
      document.getElementById('submitBtn').disabled = false;
      document.getElementById('loadingOverlay').classList.remove('active');
      _stopThinkingWords();
    }
  }

  function renderResults(result) {
    const score = result.score;
    const bd = result.score_breakdown || {};
    const cfg = TRACK_CONFIG[state.currentTrack];

    const display = document.getElementById('scoreDisplay');
    display.className = 'score-display ' + scoreClass(score);

    document.getElementById('resultScore').textContent = score;
    document.getElementById('scoreTitle').textContent = scoreLabel(score);
    document.getElementById('scoreSubtitle').textContent = cfg.scoreSubtitle;
    document.getElementById('xpEarned').textContent = result.xp_earned;

    document.getElementById('bClarity').textContent = bd.clarity ?? '-';
    document.getElementById('bContext').textContent = bd.context ?? '-';
    document.getElementById('bStructure').textContent = bd.structure ?? '-';
    document.getElementById('bOutput').textContent = bd.output_quality ?? '-';

    // Keep labels in sync with current track
    _applyBreakdownLabels();

    document.getElementById('feedbackText').textContent = result.feedback || '';
    document.getElementById('tipText').textContent = result.tip || '';
    document.getElementById('comparisonText').textContent = result.model_comparison || '';

    document.getElementById('responseContent').textContent = result.claude_response || '';
    document.getElementById('responseContent').classList.remove('open');
    document.getElementById('toggleChevron').classList.remove('open');

    document.getElementById('resultSection').classList.add('visible');
    document.getElementById('resultSection').scrollIntoView({ behavior: 'smooth', block: 'start' });

    // Switch to edit mode: hide Submit, show Resubmit, update section label
    const submitBtn = document.getElementById('submitBtn');
    const retryBtn = document.getElementById('retryBtn');
    const titleEl = document.getElementById('promptSectionTitle');
    const descEl = document.getElementById('promptDescription');
    if (submitBtn) submitBtn.style.display = 'none';
    if (retryBtn) retryBtn.style.display = '';
    if (titleEl) titleEl.textContent = '✏️ Edit your prompt and try again';
    if (descEl) descEl.textContent = 'Update your prompt above and click Resubmit to improve your score.';
  }

  function hideResults() {
    document.getElementById('resultSection').classList.remove('visible');
    // Restore submit mode
    const submitBtn = document.getElementById('submitBtn');
    const retryBtn = document.getElementById('retryBtn');
    if (submitBtn) submitBtn.style.display = '';
    if (retryBtn) retryBtn.style.display = 'none';
  }

  function toggleResponse() {
    const content = document.getElementById('responseContent');
    const chevron = document.getElementById('toggleChevron');
    content.classList.toggle('open');
    chevron.classList.toggle('open');
  }

  // ── Leaderboard ───────────────────────────────────────────────────────────

  async function renderLeaderboard() {
    const track = state.currentTrack;
    const data = await api('/api/leaderboard?track=' + track);
    const body = document.getElementById('lbBody');
    body.innerHTML = '';

    const isTrack = track !== 'all';
    const trackLabel = track === 'copilot' ? 'Copilot' : 'Claude';
    document.getElementById('lbSubtitle').textContent =
      `Top ${trackLabel} practitioners on your team`;
    document.getElementById('lbXpHeader').textContent =
      isTrack ? trackLabel + ' XP' : 'XP';

    if (!data.length) {
      body.innerHTML = '<div class="empty-state"><div class="empty-icon">🏆</div><h3>No scores yet</h3><p>Be the first to complete a challenge!</p></div>';
      return;
    }

    for (const player of data) {
      const isMe = player.username === state.username;
      const row = document.createElement('div');
      row.className = 'lb-row' + (isMe ? ' highlight' : '');

      const rankClass = player.rank === 1 ? 'gold' : player.rank === 2 ? 'silver' : player.rank === 3 ? 'bronze' : '';
      const rankSymbol = player.rank === 1 ? '🥇' : player.rank === 2 ? '🥈' : player.rank === 3 ? '🥉' : player.rank;

      const initials = player.username.substring(0, 2).toUpperCase();
      const hue = hashColor(player.username);
      const displayXp = isTrack ? player.track_xp : player.xp;

      row.innerHTML = `
        <div class="lb-rank ${rankClass}">${rankSymbol}</div>
        <div class="lb-user">
          <div class="lb-avatar" style="background:hsl(${hue},65%,45%)">${initials}</div>
          <div>
            <div class="lb-username">${player.username}${isMe ? ' <span style="color:var(--accent2);font-size:0.7rem">(you)</span>' : ''}</div>
            <div class="lb-level-name" style="color:${player.level_color}">${player.level_name}</div>
          </div>
        </div>
        <div class="lb-xp">${displayXp.toLocaleString()}</div>
        <div class="lb-challenges" style="text-align:center">${player.challenges_completed}</div>
        <div class="lb-avg" style="color:${scoreColor(player.avg_score)}">${player.avg_score > 0 ? player.avg_score : '—'}</div>
      `;
      body.appendChild(row);
    }
  }

  // ── Badges ────────────────────────────────────────────────────────────────

  function renderBadges() {
    if (!state.user) return;
    const earned = new Set(state.user.badges.map(b => b.badge_id));
    const grid = document.getElementById('badgesGrid');
    grid.innerHTML = '';

    for (const [id, badge] of Object.entries(state.badges)) {
      const isEarned = earned.has(id);
      const el = document.createElement('div');
      el.className = 'badge-item' + (isEarned ? ' earned' : '');
      el.innerHTML = `
        <div class="badge-icon">${isEarned ? badge.icon : '🔒'}</div>
        <div class="badge-name">${badge.name}</div>
        <div class="badge-desc">${badge.description}</div>
        ${isEarned ? '<div style="font-size:0.7rem;color:var(--green);margin-top:6px">✓ Earned</div>' : ''}
      `;
      grid.appendChild(el);
    }
  }

  // ── Badge Toast ───────────────────────────────────────────────────────────

  function showBadgeToasts(badges) {
    let delay = 500;
    for (const badge of badges) {
      setTimeout(() => {
        document.getElementById('toastIcon').textContent = badge.icon || '🏅';
        document.getElementById('toastName').textContent = badge.name;
        document.getElementById('toastDesc').textContent = badge.description;
        const toast = document.getElementById('badgeToast');
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 4000);
      }, delay);
      delay += 4500;
    }
  }

  // ── Helpers ───────────────────────────────────────────────────────────────

  function scoreClass(score) {
    if (score >= 85) return 'score-excellent';
    if (score >= 65) return 'score-good';
    if (score >= 45) return 'score-ok';
    return 'score-low';
  }

  function scoreLabel(score) {
    if (score >= 90) return '🏆 Outstanding!';
    if (score >= 80) return '⭐ Excellent work!';
    if (score >= 65) return '👍 Good effort!';
    if (score >= 50) return '📈 Decent start!';
    return '💪 Keep practicing!';
  }

  function scoreColor(score) {
    if (score >= 80) return 'var(--green)';
    if (score >= 60) return 'var(--yellow)';
    if (score > 0) return 'var(--red)';
    return 'var(--text-muted)';
  }

  function hashColor(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) hash = str.charCodeAt(i) + ((hash << 5) - hash);
    return Math.abs(hash) % 360;
  }

  async function api(path, method = 'GET', body = null) {
    const opts = {
      method,
      headers: { 'Content-Type': 'application/json' },
    };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(path, opts);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Unknown error' }));
      const msg = Array.isArray(err.detail)
        ? err.detail.map(e => e.msg).join(', ')
        : (err.detail || 'Request failed');
      throw new Error(msg);
    }
    return res.json();
  }

  function showFormError(id, msg) {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = msg;
    el.style.display = msg ? 'block' : 'none';
  }

  function togglePassword(inputId, btn) {
    const input = document.getElementById(inputId);
    if (!input) return;
    const showing = input.type === 'text';
    input.type = showing ? 'password' : 'text';
    btn.textContent = showing ? '👁' : '🙈';
    btn.setAttribute('aria-label', showing ? 'Show password' : 'Hide password');
  }

  // ── Admin ─────────────────────────────────────────────────────────────────

  async function loadAdminUsers() {
    const body = document.getElementById('adminBody');
    if (!body) return;
    if (!state.user?.is_admin) {
      body.innerHTML = '<div class="empty-state"><div class="empty-icon">🔒</div><h3>Access denied</h3></div>';
      return;
    }
    try {
      _adminUsers = await api('/api/admin/users?admin=' + encodeURIComponent(state.username));
      renderAdminUsers(_adminUsers);
    } catch (e) {
      body.innerHTML = '<div class="empty-state"><p>Error loading users: ' + e.message + '</p></div>';
    }
  }

  function filterAdminUsers() {
    const q = (document.getElementById('adminSearch')?.value || '').toLowerCase();
    const filtered = _adminUsers.filter(u =>
      u.username.toLowerCase().includes(q) ||
      (u.display_name || '').toLowerCase().includes(q)
    );
    renderAdminUsers(filtered);
  }

  function renderAdminUsers(users) {
    const body = document.getElementById('adminBody');
    if (!body) return;
    body.innerHTML = '';
    if (!users.length) {
      body.innerHTML = '<div class="empty-state"><p>No users found.</p></div>';
      return;
    }
    for (const u of users) {
      const isMe = u.username === state.username;
      const row = document.createElement('div');
      row.className = 'admin-row' + (isMe ? ' admin-row-me' : '') + (u.disabled ? ' admin-row-disabled' : '');
      row.innerHTML = `
        <div class="admin-user-cell">
          <strong>${u.username}</strong>${isMe ? ' <span class="admin-you-tag">(you)</span>' : ''}
          <span class="admin-display-name">${u.display_name || ''}</span>
        </div>
        <div style="text-align:right;font-variant-numeric:tabular-nums">${(u.xp || 0).toLocaleString()}</div>
        <div style="text-align:center">
          <button class="admin-toggle ${u.claude_access ? 'admin-toggle-on' : 'admin-toggle-off'}"
            onclick="App.togglePermission('${u.username}', 'claude_access', ${!u.claude_access})">
            ${u.claude_access ? 'Yes' : 'No'}
          </button>
        </div>
        <div style="text-align:center">
          <button class="admin-toggle ${u.is_admin ? 'admin-toggle-on' : 'admin-toggle-off'}"
            onclick="App.togglePermission('${u.username}', 'is_admin', ${!u.is_admin})">
            ${u.is_admin ? 'Admin' : 'Operator'}
          </button>
        </div>
        <div style="text-align:center">
          <button class="admin-toggle ${u.disabled ? 'admin-toggle-off' : 'admin-toggle-on'}"
            onclick="App.togglePermission('${u.username}', 'disabled', ${!u.disabled})">
            ${u.disabled ? 'Disabled' : 'Active'}
          </button>
        </div>
        <div class="admin-actions-cell">
          <button class="admin-action-btn admin-pw-btn" onclick="App.changeUserPassword('${u.username}')" title="Reset password">🔑</button>
          ${isMe ? '' : `<button class="admin-action-btn admin-delete-btn" onclick="App.deleteUser('${u.username}')" title="Delete user">🗑</button>`}
        </div>
      `;
      body.appendChild(row);
    }
  }

  async function togglePermission(targetUsername, field, value) {
    try {
      await api(
        '/api/admin/users/' + encodeURIComponent(targetUsername) + '/permissions?admin=' + encodeURIComponent(state.username),
        'PUT',
        { [field]: value }
      );
      await loadAdminUsers();
    } catch (e) {
      alert('Error updating permissions: ' + e.message);
    }
  }

  async function changeUserPassword(targetUsername) {
    const newPassword = prompt(`Set new password for "${targetUsername}" (min 6 characters):`);
    if (newPassword === null) return;
    if (newPassword.length < 6) {
      alert('Password must be at least 6 characters.');
      return;
    }
    try {
      await api(
        '/api/admin/users/' + encodeURIComponent(targetUsername) + '/password?admin=' + encodeURIComponent(state.username),
        'PUT',
        { new_password: newPassword }
      );
      alert('Password updated for ' + targetUsername + '.');
    } catch (e) {
      alert('Error: ' + e.message);
    }
  }

  async function deleteUser(targetUsername) {
    if (!confirm(`Permanently delete "${targetUsername}"? This removes all their submissions and badges and cannot be undone.`)) return;
    try {
      await api(
        '/api/admin/users/' + encodeURIComponent(targetUsername) + '?admin=' + encodeURIComponent(state.username),
        'DELETE'
      );
      await loadAdminUsers();
    } catch (e) {
      alert('Error deleting user: ' + e.message);
    }
  }

  // ── Public API ────────────────────────────────────────────────────────────

  document.addEventListener('DOMContentLoaded', init);

  return {
    login,
    logout,
    register,
    showView,
    openChallenge,
    submitChallenge,
    revealHint,
    updateCharCount,
    toggleResponse,
    switchTrack,
    togglePassword,
    filterAdminUsers,
    togglePermission,
    changeUserPassword,
    deleteUser,
  };
})();
