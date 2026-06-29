const App = (() => {
  let state = {
    username: null,
    user: null,
    challenges: [],
    categories: {},
    badges: {},
    currentChallenge: null,
    modelPromptRevealed: false,
    currentTrack: 'claude',
    loginMode: 'login',
  };

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

  function switchLoginMode(mode) {
    state.loginMode = mode;
    document.getElementById('formLogin').style.display = mode === 'login' ? '' : 'none';
    document.getElementById('formRegister').style.display = mode === 'register' ? '' : 'none';
    document.getElementById('tabLogin').classList.toggle('active', mode === 'login');
    document.getElementById('tabRegister').classList.toggle('active', mode === 'register');
  }

  async function login() {
    const username = document.getElementById('usernameInput').value.trim();
    const password = document.getElementById('passwordInput').value;
    if (!username) { document.getElementById('usernameInput').focus(); return; }
    if (!password) { document.getElementById('passwordInput').focus(); return; }
    try {
      const user = await api('/api/users', 'POST', { username, password });
      state.username = username;
      state.user = user;
      localStorage.setItem('ct_username', username);
      await loadChallenges();
      showNav();
      renderDashboard();
      showView('dashboard');
    } catch (e) {
      alert('Sign in failed: ' + e.message);
    }
  }

  async function register() {
    const displayName = document.getElementById('regDisplayName').value.trim();
    const username = document.getElementById('regUsername').value.trim();
    const email = document.getElementById('regEmail').value.trim();
    const password = document.getElementById('regPassword').value;
    if (!username) { document.getElementById('regUsername').focus(); return; }
    if (!email) { document.getElementById('regEmail').focus(); return; }
    if (!password) { document.getElementById('regPassword').focus(); return; }
    try {
      const user = await api('/api/register', 'POST', { username, email, password, display_name: displayName || username });
      state.username = username;
      state.user = user;
      localStorage.setItem('ct_username', username);
      await loadChallenges();
      showNav();
      renderDashboard();
      showView('dashboard');
    } catch (e) {
      alert('Registration failed: ' + e.message);
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
    state.currentTrack = 'claude';
    state.loginMode = 'login';
    document.getElementById('nav').style.display = 'none';
    document.getElementById('usernameInput').value = '';
    document.getElementById('passwordInput').value = '';
    document.getElementById('regDisplayName').value = '';
    document.getElementById('regUsername').value = '';
    document.getElementById('regEmail').value = '';
    document.getElementById('regPassword').value = '';
    switchLoginMode('login');
    showView('login');
    document.getElementById('usernameInput').focus();
  }

  // ── Track switching ───────────────────────────────────────────────────────

  async function switchTrack(track) {
    if (state.currentTrack === track) return;
    state.currentTrack = track;
    _applyTrackUI();
    await loadChallenges();
    showView('dashboard');
  }

  function _applyTrackUI() {
    const cfg = TRACK_CONFIG[state.currentTrack];
    document.getElementById('navLogo').textContent = cfg.logo;
    document.getElementById('trackBtnClaude').classList.toggle('active', state.currentTrack === 'claude');
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

    if (name === 'dashboard') renderDashboard();
    else if (name === 'leaderboard') renderLeaderboard();
    else if (name === 'badges') renderBadges();
  }

  // ── Nav ───────────────────────────────────────────────────────────────────

  function showNav() {
    document.getElementById('nav').style.display = 'flex';
    _applyTrackUI();
    updateNav();
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
    state.modelPromptRevealed = false;

    document.getElementById('detailCategory').textContent = challenge.category_label;
    document.getElementById('detailDifficulty').textContent = challenge.difficulty;
    document.getElementById('detailXp').textContent = challenge.xp_reward;
    document.getElementById('detailTitle').textContent = challenge.icon + ' ' + challenge.title;
    document.getElementById('detailScenario').textContent = challenge.scenario;
    document.getElementById('detailContext').textContent = challenge.context || '';

    const tipsList = document.getElementById('tipsList');
    tipsList.innerHTML = '';
    for (const tip of (challenge.what_makes_a_great_prompt || [])) {
      const li = document.createElement('li');
      li.textContent = tip;
      tipsList.appendChild(li);
    }

    document.getElementById('promptInput').value = '';
    document.getElementById('charCount').textContent = '0 characters';
    document.getElementById('revealBtn').textContent = '👁 Reveal Model Prompt';
    document.getElementById('modelPromptReveal').classList.remove('visible');
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

  function revealModelPrompt() {
    const c = state.currentChallenge;
    if (!c) return;
    state.modelPromptRevealed = true;
    document.getElementById('modelPromptText').textContent = c.model_prompt || '';
    document.getElementById('modelPromptReveal').classList.add('visible');
    document.getElementById('revealBtn').textContent = '✓ Model Prompt Revealed';
    document.getElementById('revealBtn').disabled = true;
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
    hideResults();

    try {
      const result = await api(
        '/api/challenges/' + state.currentChallenge.id + '/submit',
        'POST',
        { username: state.username, prompt }
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
  }

  function hideResults() {
    document.getElementById('resultSection').classList.remove('visible');
  }

  function toggleResponse() {
    const content = document.getElementById('responseContent');
    const chevron = document.getElementById('toggleChevron');
    content.classList.toggle('open');
    chevron.classList.toggle('open');
  }

  // ── Leaderboard ───────────────────────────────────────────────────────────

  async function renderLeaderboard() {
    const data = await api('/api/leaderboard');
    const body = document.getElementById('lbBody');
    body.innerHTML = '';

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

      row.innerHTML = `
        <div class="lb-rank ${rankClass}">${rankSymbol}</div>
        <div class="lb-user">
          <div class="lb-avatar" style="background:hsl(${hue},65%,45%)">${initials}</div>
          <div>
            <div class="lb-username">${player.username}${isMe ? ' <span style="color:var(--accent2);font-size:0.7rem">(you)</span>' : ''}</div>
            <div class="lb-level-name" style="color:${player.level_color}">${player.level_name}</div>
          </div>
        </div>
        <div class="lb-xp">${player.xp.toLocaleString()}</div>
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
      throw new Error(err.detail || 'Request failed');
    }
    return res.json();
  }

  // ── Public API ────────────────────────────────────────────────────────────

  document.addEventListener('DOMContentLoaded', init);

  return {
    login,
    logout,
    register,
    switchLoginMode,
    showView,
    openChallenge,
    submitChallenge,
    revealModelPrompt,
    updateCharCount,
    toggleResponse,
    switchTrack,
  };
})();
