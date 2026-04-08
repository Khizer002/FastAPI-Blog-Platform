<h1>FastAPI Blog Platform</h1>

<p>Hey! This is a solid REST API for a blog site I built using FastAPI and MySQL. It's got everything: users, posts, and a voting system. I really focused on making this "production-ready," so it's fully <strong>Async</strong>, uses structured logging, and keeps an eye on performance with Sentry monitoring.</p>

<h2>What’s inside?</h2>
<p>You can sign up, log in, write blogs, and like/unlike posts. It’s built to be fast, using <strong>Async/Await</strong> so the database doesn't get choked up when multiple people are using it. It's currently live on Railway!</p>

<h2>Cool Tech Features</h2>
<ul>
<li><strong>Better Security (JWT Refresh Tokens):</strong> I upgraded the login system. Now, instead of just one token, you get a pair. When your short-term access dies, the app automatically uses a "Refresh Token" to keep you logged in without making you type your password again.</li>
<li><strong>Rate Limiting (No Spam):</strong> Added a bouncer to the API. If someone tries to spam the login or refresh routes, the app slows them down so the server stays safe.</li>
<li><strong>Super Fast (Async Everything):</strong> Everything from database calls (SQLAlchemy 2.0 + aiomysql) to logging is asynchronous.</li>
<li><strong>Smart Logging:</strong> Used <code>Loguru</code>. It prints detailed debug stuff in my terminal but saves clean, easy-to-read success logs in a file for later.</li>
<li><strong>Error Tracking:</strong> Integrated <strong>Sentry</strong>. If something breaks, I get an alert immediately so I can fix it.</li>
<li><strong>Package Management:</strong> Swapped standard pip for <code>uv</code>. It installs dependencies almost instantly.</li>
</ul>

<h2>The Tech Stack</h2>
<p><strong>Framework:</strong> FastAPI (Async)</p>
<p><strong>Package Manager:</strong> uv (Super fast!)</p>
<p><strong>Database:</strong> MySQL 8.0 with SQLAlchemy 2.0 (Async mode)</p>
<p><strong>Monitoring:</strong> Sentry SDK</p>
<p><strong>Security:</strong> JWT with Refresh Token Rotation & Argon2 hashing</p>

<h2>API Endpoints</h2>
<h3>Auth & Users</h3>
<ul>
<li><code>POST /login</code> - Get your tokens</li>
<li><code>POST /refresh</code> - Use your refresh token to stay logged in</li>
<li><code>POST /users</code> - Create an account</li>
<li><code>GET /users/{id}</code> - Check user details</li>
</ul>

<h3>The Fun Stuff</h3>
<ul>
<li><code>GET /blogs</code> - See all posts (with search and pagination)</li>
<li><code>POST /blogs</code> - Write a new post</li>
<li><code>PUT /blogs/{id}</code> - Edit your post</li>
<li><code>DELETE /blogs/{id}</code> - Delete a post</li>
<li><code>POST /vote</code> - Like or unlike a blog</li>
</ul>

<h2>How to run it locally</h2>
<pre><code># Clone it
git clone https://github.com/Khizer002/FastAPI-Blog-Platform.git
cd FastAPI-Blog-Platform

# Sync your environment (this is fast thanks to uv)
uv sync

# Set up your .env with your DB info and run migrations
uv run alembic upgrade head

# Fire it up!
uv run uvicorn app.main1:app --reload
</code></pre>

<h2>Project Structure</h2>
<pre><code>FastAPI-Blog-Platform/
├── app/
│   ├── routers/          # Async API route handlers with integrated Loguru
│   ├── database.py       # Async MySQL connection & session management
│   ├── models.py         # SQLAlchemy 2.0 ORM models
│   ├── schemas.py        # Pydantic models for validation
│   ├── oauth2.py         # Async JWT logic & Auth dependencies
│   └── config.py         # Pydantic Settings for .env management
└── logs/                 # Persistent app logs (SUCCESS level)
</code></pre>

<h2>Contact</h2>
<p>Khizer Ahmad - <a href="https://github.com/Khizer002">GitHub Profile</a></p>