<h1>FastAPI Blog Platform</h1>

<p>A RESTful API backend for a blog platform built with FastAPI and MySQL, featuring user authentication, CRUD operations, and a voting system. This project follows modern production standards, including <strong>Asynchronous programming</strong>, structured logging, and performance monitoring.</p>

<h2>Overview</h2>
<p>This project is a fully functional blog API that allows users to register, authenticate, create blog posts, and interact with content through a voting system. It demonstrates modern backend development practices with Python, utilizing <strong>Async/Await</strong> for high-performance database interactions, and is deployed on Railway for production use.</p>

<h2>Key Features</h2>
<ul>
<li><strong>Asynchronous Architecture:</strong> Fully migrated to <code>Async/Await</code> using <code>SQLAlchemy 2.0</code> and <code>aiomysql</code> to handle concurrent requests efficiently without blocking the event loop.</li>
<li><strong>Structured Logging:</strong> Implemented <code>Loguru</code> for high-performance, asynchronous logging. Configured with separate sinks for a detailed <code>DEBUG</code> terminal and a clean, <code>SUCCESS</code>-level <code>app.log</code> for production audits.</li>
<li><strong>Error Monitoring:</strong> Integrated <strong>Sentry</strong> for real-time error tracking and performance monitoring, ensuring zero-downtime visibility.</li>
<li><strong>Modern Dependency Injection:</strong> Uses <code>Annotated</code> types for cleaner, more readable code in routers and dependencies, paired with <code>async_sessionmaker</code> for session management.</li>
<li><strong>High-Performance Tooling:</strong> Managed with <code>uv</code> for lightning-fast environment setup and dependency resolution.</li>
<li><strong>Security First:</strong> JWT authentication with safe <code>.get()</code> payload handling and Bcrypt password hashing.</li>
<li><strong>Advanced CRUD:</strong> Supports pagination, search filters, and relational data (Post likes/votes) using <code>selectinload</code> for optimized async loading.</li>
</ul>

<h2>Technology Stack</h2>
<p><strong>Backend Framework:</strong> FastAPI (Async)</p>
<p><strong>Package Manager:</strong> uv (Replacing standard pip)</p>
<p><strong>Logging:</strong> Loguru</p>
<p><strong>Monitoring:</strong> Sentry SDK</p>
<p><strong>Database:</strong> MySQL 8.0</p>
<p><strong>ORM:</strong> SQLAlchemy 2.0 (Async Mode)</p>
<p><strong>Database Driver:</strong> aiomysql</p>
<p><strong>Authentication:</strong> JWT (PyJWT)</p>

<h2>API Endpoints</h2>
<h3>Authentication</h3>
<ul>
<li><code>POST /login</code> - Authenticate and receive access token</li>
<li><code>POST /users</code> - Register a new account</li>
</ul>

<h3>Blog Posts</h3>
<ul>
<li><code>GET /blogs</code> - Retrieve all blog posts (supports async pagination & search)</li>
<li><code>GET /blogs/{id}</code> - Retrieve a specific blog post</li>
<li><code>POST /blogs</code> - Create a new blog post</li>
<li><code>PUT /blogs/{id}</code> - Update a blog post</li>
<li><code>DELETE /blogs/{id}</code> - Delete a blog post</li>
</ul>

<h3>Votes</h3>
<ul>
<li><code>POST /vote</code> - Like or unlike a blog post (Async execution)</li>
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

Sync environment using uv (installs aiomysql and sqlalchemy 2.0)
uv sync

Setup .env file with DATABASE_URL (use mysql+aiomysql://) and SENTRY_DSN
Then run migrations:
uv run alembic upgrade head

Start the async server
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