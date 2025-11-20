<!DOCTYPE html>
<html lang="en">
<body>

<header>
  <h1>SkillLink <small>— The Skill Exchange Network</small></h1>
  <p><strong>Version:</strong> 1.0 &nbsp;|&nbsp; <strong>Repo:</strong> <a href="https://github.com/muneeb-shafique/SkillLink/">github.com/muneeb-shafique/SkillLink/</a></p>
  <p><strong>Maintainers:</strong> Muneeb (2024-DS-36), Dayyan (2024-DS-24), Huzaifa (2024-DS-47), Jawad (2024-DS-18)</p>
  <time datetime="2025-11-20">Updated: 2025-11-20</time>
</header>

<nav aria-label="main navigation">
  <ul>
    <li><a href="#project-brief">Project Brief</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#quickstart">Quick Start</a></li>
    <li><a href="#api">API</a></li>
    <li><a href="#data-model">Data Model</a></li>
    <li><a href="#architecture">Architecture</a></li>
    <li><a href="#deployment">Deployment</a></li>
    <li><a href="#testing">Testing & CI</a></li>
    <li><a href="#metrics">Metrics</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#faq">FAQ</a></li>
  </ul>
</nav>

<hr>

<section id="project-brief">
  <h2>Project Brief</h2>
  <p><mark>SkillLink</mark> is a peer-to-peer web platform for exchanging skills without monetary transactions. Users post skills they can teach and skills they want to learn; the system suggests matches, supports scheduling, real-time chat, and reputation mechanics.</p>

  <figure>
    <svg role="img" viewBox="0 0 200 60" width="320" height="96" xmlns="http://www.w3.org/2000/svg" aria-labelledby="logoTitle logoDesc">
      <title id="logoTitle">SkillLink logo</title>
      <desc id="logoDesc">abstract network icon with nodes and connecting lines</desc>
      <circle cx="20" cy="30" r="6" />
      <circle cx="80" cy="15" r="6" />
      <circle cx="120" cy="40" r="6" />
      <circle cx="170" cy="20" r="6" />
      <line x1="20" y1="30" x2="80" y2="15" stroke-width="2" />
      <line x1="80" y1="15" x2="120" y2="40" stroke-width="2" />
      <line x1="120" y1="40" x2="170" y2="20" stroke-width="2" />
    </svg>
    <figcaption>Conceptual network logo — nodes represent users connecting via skills.</figcaption>
  </figure>
</section>

<hr>

<section id="features">
  <h2>Features (exhaustive)</h2>

  <dl>
    <dt>Authentication & Identity</dt>
    <dd>
      <ul>
        <li>Email/password + OAuth (Google, GitHub)</li>
        <li>Verification, password reset, optional 2FA (TOTP)</li>
        <li>Account-level privacy controls and export/delete endpoints</li>
      </ul>
    </dd>

 <dt>Profile & Skills</dt>
    <dd>
      <ul>
        <li>Multiple skill entries with: title, category, proficiency, tags, availability, timezone</li>
        <li>Attachments support (portfolio links, sample files)</li>
        <li>Profile badges, verification flags, and average rating</li>
      </ul>
    </dd>

 <dt>Matching Engine</dt>
    <dd>
      <ul>
        <li>Pluggable scoring: TF-IDF, embeddings, availability overlap, proximity, social proof</li>
        <li>Explainable match reasons (why this match?) for transparency</li>
        <li>Batch recommendations + live stream suggestions</li>
      </ul>
    </dd>

 <dt>Real-time Communication</dt>
    <dd>
      <ul>
        <li>WebSocket chat with read receipts and typing indicators</li>
        <li>Optional integration with third-party video providers</li>
        <li>Message soft-delete + audit logs for moderation</li>
      </ul>
    </dd>

 <dt>Session Flow</dt>
    <dd>
      <ul>
        <li>Session proposals, scheduling, calendar sync (ICS export)</li>
        <li>Session lifecycle: proposed → accepted → completed → rated</li>
      </ul>
    </dd>

 <dt>Ratings, Moderation & Safety</dt>
    <dd>
      <ul>
        <li>Per-session ratings with textual feedback and automated abuse flags</li>
        <li>Admin moderation console with audit trail</li>
        <li>Safety features: report, block, verified user flows</li>
      </ul>
    </dd>

<dt>Notifications & Emails</dt>
    <dd>
      <ul>
        <li>In-app notifications, email digests, optional push</li>
        <li>Rate-limited and digest-mode to reduce spam</li>
      </ul>
    </dd>
  </dl>
</section>

<hr>

<section id="quickstart">
  <h2>Quick Start</h2>

  <h3>Clone & Setup</h3>
  <pre><code>git clone https://github.com/muneeb-shafique/SkillLink/
cd SkillLink</code></pre>

  <h3>Backend (example: Node.js)</h3>
  <pre><code>cd backend
cp .env.example .env
# fill credentials
npm install
npm run migrate
npm run seed
npm run dev</code></pre>

  <h3>Frontend (example: React)</h3>
  <pre><code>cd ../frontend
npm install
npm run dev</code></pre>

  <h3>Health Check</h3>
  <pre><code>curl http://localhost:4000/api/v1/health
# expected: {"status":"ok","uptime":...}</code></pre>

  <form action="#" method="post" aria-label="example contact form">
    <fieldset>
      <legend>Example contact (demo only)</legend>
      <label for="demo-name">Name:</label>
      <input id="demo-name" name="name" type="text" placeholder="Your name" disabled>
      <label for="demo-email">Email:</label>
      <input id="demo-email" name="email" type="email" placeholder="you@example.com" disabled>
      <input type="submit" value="Submit" disabled>
    </fieldset>
  </form>
</section>

<hr>

<section id="api">
  <h2>API Reference — Core Endpoints</h2>

  <table border="1" cellpadding="6" cellspacing="0">
    <thead>
      <tr>
        <th>Endpoint</th>
        <th>Method</th>
        <th>Auth</th>
        <th>Notes</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>/api/v1/auth/register</td><td>POST</td><td>No</td><td>Registers user; sends verification email.</td></tr>
      <tr><td>/api/v1/auth/login</td><td>POST</td><td>No</td><td>Returns JWT + refresh token.</td></tr>
      <tr><td>/api/v1/skills</td><td>GET / POST</td><td>GET public / POST auth</td><td>List or create skill items.</td></tr>
      <tr><td>/api/v1/matches</td><td>GET / POST</td><td>Auth</td><td>Get recommended matches / propose match.</td></tr>
      <tr><td>/api/v1/chats/:id/messages</td><td>GET / POST</td><td>Auth</td><td>Message history & send message.</td></tr>
      <tr><td>/api/v1/admin/reports</td><td>GET / POST</td><td>Admin</td><td>Moderation endpoints</td></tr>
    </tbody>
  </table>

  <h3>Sample Request (curl)</h3>
  <pre><code>curl -X POST http://localhost:4000/api/v1/skills \
  -H "Authorization: Bearer &lt;token&gt;" \
  -H "Content-Type: application/json" \
  -d '{"title":"Intro to SQL","category":"databases","level":"beginner"}'</code></pre>

  <details>
    <summary>Authentication details</summary>
    <p>Use short-lived access tokens (JWT) and long-lived refresh tokens. Revoke refresh tokens on password change.</p>
  </details>
</section>

<hr>

<section id="data-model">
  <h2>Data Model</h2>

  <table border="1" cellpadding="6" cellspacing="0">
    <caption>Primary entities</caption>
    <thead><tr><th>Entity</th><th>Key fields</th><th>Relations</th></tr></thead>
    <tbody>
      <tr><td>User</td><td>id, name, email, password_hash, rating_avg, created_at</td><td>1-to-many: Skill, Message, Review</td></tr>
      <tr><td>Skill</td><td>id, owner_id, title, category, level, tags[], availability</td><td>belongs to User</td></tr>
      <tr><td>Match</td><td>id, user_a, user_b, score, status</td><td>references two Users</td></tr>
      <tr><td>Message</td><td>id, chat_id, sender_id, content, ts</td><td>belongs to Chat</td></tr>
      <tr><td>Review</td><td>id, from_id, to_id, rating, text</td><td>user-to-user</td></tr>
    </tbody>
  </table>

  <h3>SQL Snippets</h3>
  <pre><code>CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(200),
  email VARCHAR(255) UNIQUE,
  password_hash VARCHAR(255),
  rating_avg NUMERIC(3,2) DEFAULT 0,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE skills (
  id SERIAL PRIMARY KEY,
  owner_id INT REFERENCES users(id),
  title VARCHAR(255),
  category VARCHAR(100),
  level VARCHAR(50),
  tags TEXT[],
  availability JSONB,
  created_at TIMESTAMP DEFAULT now()
);</code></pre>
</section>

<hr>

<section id="architecture">
  <h2>Architecture</h2>

  <ol>
    <li><strong>Client:</strong> SPA (React/Vue) + server-side-rendered marketing pages</li>
    <li><strong>API:</strong> REST + optional GraphQL layer for complex queries</li>
    <li><strong>Realtime:</strong> WebSocket service for chat & live events</li>
    <li><strong>Worker:</strong> Background job processor for emails, match recalcs</li>
    <li><strong>Storage:</strong> Postgres (primary), Redis (cache/queue), S3 (blobs)</li>
  </ol>

  <h3>Resilience patterns</h3>
  <ul>
    <li>Retries with exponential backoff</li>
    <li>Bulkhead isolation for workers</li>
    <li>Graceful degradation for search (fallback to DB)</li>
  </ul>

  <h3>Diagram (ASCII)</h3>
  <pre><code>Browser (SPA)
     |
  Load Balancer
   /    \
 API   WebSocket
  |       |
 Postgres  Redis
   \      /
   Workers</code></pre>
</section>

<hr>

<section id="deployment">
  <h2>Deployment</h2>

  <h3>Checklist</h3>
  <ul>
    <li>HTTPS & HSTS</li>
    <li>Secrets in vault (no secrets in repo)</li>
    <li>DB backups & PITR</li>
    <li>Monitoring (Prometheus/Grafana) & error reporting (Sentry)</li>
    <li>Auto-scaling policies for API & WS</li>
  </ul>

  <h3>Docker Compose (example)</h3>
  <pre><code>version: '3.8'
services:
  db:
    image: postgres:15
  redis:
    image: redis:7
  api:
    build: ./backend
    depends_on: [db, redis]</code></pre>
</section>

<hr>

<section id="testing">
  <h2>Testing & CI</h2>

  <p>Recommended pipeline:</p>
  <ol>
    <li>Linting (ESLint / Flake8)</li>
    <li>Unit tests (Jest / PyTest)</li>
    <li>Integration tests (supertest / requests)</li>
    <li>End-to-end (Cypress / Playwright)</li>
    <li>Security scanning and dependency checks</li>
  </ol>

  <h3>GitHub Actions snippet</h3>
  <pre><code>name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 18
      - run: npm ci
      - run: npm test -- --coverage</code></pre>
</section>

<hr>

<section id="metrics">
  <h2>Product Metrics</h2>

  <meter value="0.7" min="0" max="1">Core features readiness: 70%</meter>
  <p>Track:</p>
  <ul>
    <li>DAU / MAU</li>
    <li>Matches created</li>
    <li>Session completion rate</li>
    <li>Avg rating & NPS</li>
  </ul>
</section>

<hr>

<section id="contributing">
  <h2>Contributing</h2>

  <p>Please follow the workflow:</p>
  <ol>
    <li>Fork the repo</li>
    <li>Create a branch: <kbd>feature/your-idea</kbd></li>
    <li>Run tests locally</li>
    <li>Open a PR with a clear title and description</li>
    <li>Link the PR to an issue if applicable</li>
  </ol>

  <h3>Commit message format</h3>
  <pre><code>feat: add matchmaking endpoint
fix: resolve null pointer during skill create
docs: update README</code></pre>

  <details>
    <summary>Code of Conduct</summary>
    <p>Be respectful. No harassment. Treat maintainers and contributors kindly.</p>
  </details>
</section>

<hr>

<section id="faq">
  <h2>FAQ</h2>
  <dl>
    <dt>Is SkillLink free?</dt>
    <dd>Yes, core features are free. Any optional premium features will be opt-in.</dd>

 <dt>How do I report abuse?</dt>
    <dd>Use the report button on a profile or message. Admins review reports with audit logs.</dd>

 <dt>Can I migrate my data?</dt>
    <dd>Yes — the platform offers data export (JSON/CSV) and account deletion endpoints.</dd>
  </dl>
</section>

<hr>

<section id="legal">
  <h2>Legal & License</h2>
  <p>Licensed under the MIT License. See <a href="LICENSE">LICENSE</a> for full text.</p>
  <address>
    This project is made and maintained under Institute of Data Science, University of Engineering and Technology(UET) Lahore as a part of 3rd semester Software Engineering Project. <strong>Contact:</strong> <a href="mailto:muneebshafiq512@gmail.com">muneebshafiq512@gmail.com</a> or <strong>Visit:<strong> <a href="https://muneebshafique.xo.je/"> My Website</a> for any kind of query or collaboration.
  </address>
</section>

<hr>

<section id="references-and-resources">
  <h2>References & Resources</h2>
  <ol>
    <li><a href="https://docs.github.com/en">GitHub Docs</a></li>
    <li><a href="https://www.postgresql.org/docs/">PostgreSQL Docs</a></li>
    <li><a href="https://developer.mozilla.org/">MDN Web Docs</a></li>
  </ol>
</section>

<footer>
  <p><strong>Drop-in README:</strong> This file is purposely verbose — keep or trim sections as repo maturity grows. To convert to <code>README.md</code> (Markdown) run a minimal manual conversion; many docs sections are already Markdown-friendly inside <code>&lt;pre&gt;&lt;code&gt;</code> blocks.</p>
  <p><small>Generated to be GitHub-friendly: use this HTML as <code>README.html</code> in the repo root and reference from <code>README.md</code> with a link if desired.</small></p>
</footer>

</body>
</html>
