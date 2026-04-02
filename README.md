<h1>FastAPI Blog Platform</h1>

<p>A RESTful API backend for a blog platform built with FastAPI and MySQL, featuring user authentication, CRUD operations, and a voting system. This project follows modern production standards, including structured logging and performance monitoring.</p>

<h2>Overview</h2>
<p>This project is a fully functional blog API that allows users to register, authenticate, create blog posts, and interact with content through a voting system. It demonstrates modern backend development practices with Python and is deployed on Railway for production use.</p>

<h2>Key Features</h2>
<ul>
<li><strong>Structured Logging:</strong> Implemented <code>Loguru</code> for high-performance, asynchronous logging. Configured with separate sinks for a detailed <code>DEBUG</code> terminal and a clean, <code>SUCCESS</code>-level <code>app.log</code> for production audits.</li>
<li><strong>Error Monitoring:</strong> Integrated <strong>Sentry</strong> for real-time error tracking and performance monitoring, ensuring zero-downtime visibility.</li>
<li><strong>Modern Dependency Injection:</strong> Uses <code>Annotated</code> types for cleaner, more readable code in routers and dependencies.</li>
<li><strong>High-Performance Tooling:</strong> Managed with <code>uv</code> for lightning-fast environment setup and dependency resolution.</li>
<li><strong>Security First:</strong> JWT authentication with safe <code>.get()</code> payload handling and Bcrypt password hashing.</li>
<li><strong>Advanced CRUD:</strong> Supports pagination, search filters, and relational data (Post likes/votes).</li>
</ul>

<h2>Technology Stack</h2>
<p><strong>Backend Framework:</strong> FastAPI</p>
<p><strong>Package Manager:</strong> uv (Replacing standard pip)</p>
<p><strong>Logging:</strong> Loguru</p>
<p><strong>Monitoring:</strong> Sentry SDK</p>
<p><strong>Database:</strong> MySQL 8.0</p>
<p><strong>ORM:</strong> SQLAlchemy 1.4.29</p>
<p><strong>Authentication:</strong> JWT (PyJWT)</p>

<h2>API Endpoints</h2>
<h3>Authentication</h3>
<ul>
<li><code>POST /login</code> - Authenticate and receive access token</li>
<li><code>POST /users</code> - Register a new account</li>
</ul>

<h3>Blog Posts</h3>
<ul>
<li><code>GET /blogs</code> - Retrieve all blog posts (supports pagination & search)</li>
<li><code>GET /blogs/{id}</code> - Retrieve a specific blog post</li>
<li><code>POST /blogs</code> - Create a new blog post</li>
<li><code>PUT /blogs/{id}</code> - Update a blog post</li>
<li><code>DELETE /blogs/{id}</code> - Delete a blog post</li>
</ul>

<h3>Votes</h3>
<ul>
<li><code>POST /vote</code> - Like or unlike a blog post</li>
</ul>

<h2>Installation and Setup</h2>
<h3>Prerequisites</h3>
<ul>
<li>Python 3.12 or higher</li>
<li>MySQL 8.0 or higher</li>
<li>uv (Install via: <code>pip install uv</code>)</li>
</ul>

<h3>Local Development</h3>
<pre><code>git clone https://github.com/Khizer002/FastAPI-Blog-Platform.git
cd FastAPI-Blog-Platform

# Sync environment using uv
uv sync

# Setup .env file with DATABASE_URL and SENTRY_DSN
# Then run migrations:
uv run alembic upgrade head

# Start the server
uv run uvicorn app.main1:app --reload
</code></pre>

<h2>Project Structure</h2>
<pre><code>FastAPI-Blog-Platform/
├── app/
│   ├── routers/          # API route handlers with integrated Loguru
│   ├── database.py       # MySQL connection & session management
│   ├── models.py         # SQLAlchemy ORM models
│   ├── schemas.py        # Pydantic models for validation
│   ├── oauth2.py         # JWT logic & Auth dependencies
│   └── config.py         # Pydantic Settings for .env management
└── logs/                 # Persistent app logs (SUCCESS level)
</code></pre>

<h2>Contact</h2>
<p>Khizer Ahmad - <a href="https://github.com/Khizer002">GitHub Profile</a></p>