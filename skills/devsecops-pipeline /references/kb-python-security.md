---
description: "Knowledge Base — Python Security"
type: "reference"
scope: "stack-specific"
stack: "Python / FastAPI / Django / Flask"
last_updated: "2025-01-01"
---

# Python Security

**Purpose:** Stack-specific secure coding guidance for Python web applications. Covers recommended libraries, secure configuration patterns, and concrete anti-patterns.

---

## 1. Recommended Security Libraries

| Category | Library | Version | Purpose | Notes |
|---|---|---|---|---|
| **Input Validation** | `pydantic` | 2.x | Data validation with type hints | Standard for FastAPI, usable anywhere |
| **Input Validation** | `marshmallow` | 3.x | Schema validation | Mature, framework-agnostic |
| **Password Hashing** | `argon2-cffi` | 23.x | Argon2id implementation | Preferred for new projects |
| **Password Hashing** | `bcrypt` | 4.x | bcrypt implementation | Widely supported alternative |
| **Password Hashing** | `passlib` | 1.7.x | Multi-algorithm password hashing | Wraps bcrypt, argon2, pbkdf2 |
| **JWT** | `PyJWT` | 2.x | JWT encode/decode | Always specify algorithms list |
| **JWT** | `python-jose` | 3.x | JOSE implementation | More comprehensive than PyJWT |
| **ORM** | `SQLAlchemy` | 2.x | SQL ORM | Parameterized by default |
| **ORM** | `Django ORM` | 5.x | Django's built-in ORM | Parameterized by default |
| **HTTP Security** | `secure` | 0.3.x | Security headers | Framework-agnostic |
| **Rate Limiting** | `slowapi` | 0.1.x | Rate limiting for FastAPI | Built on `limits` library |
| **Rate Limiting** | `django-ratelimit` | 4.x | Rate limiting for Django | Decorator-based |
| **CORS** | `fastapi.middleware.cors` | — | CORS for FastAPI | Built-in |
| **CORS** | `django-cors-headers` | 4.x | CORS for Django | Configure CORS_ALLOWED_ORIGINS |
| **Secrets** | `python-dotenv` | 1.x | Load .env files | Development only |
| **Logging** | `structlog` | 24.x | Structured logging | JSON output, processor pipeline |
| **Logging** | `python-json-logger` | 2.x | JSON formatter for stdlib logging | Lightweight |
| **Sanitization** | `bleach` | 6.x | HTML sanitization | For user-submitted HTML content |
| **Cryptography** | `cryptography` | 42.x | Cryptographic primitives | Use high-level recipes (Fernet) |
| **Random** | `secrets` (stdlib) | — | Cryptographic random | Always use over `random` module |

---

## 2. FastAPI Security Configuration

### 2.1 Application Setup

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import uuid

app = FastAPI(
    title="Secure API",
    docs_url=None if os.environ.get("ENV") == "production" else "/docs",  # Disable docs in prod
    redoc_url=None,
)

# 1. Trusted hosts
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["api.example.com", "localhost"])

# 2. CORS — explicit allowlist
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],  # NEVER use ["*"] with credentials
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True,
    max_age=86400,
)

# 3. Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 4. Request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request.state.request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response

# 5. Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers.pop("server", None)
    return response
```

### 2.2 Global Error Handler

```python
from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log full details internally
    logger.error(
        "Unhandled exception",
        extra={
            "error": str(exc),
            "path": request.url.path,
            "method": request.method,
            "request_id": getattr(request.state, "request_id", "unknown"),
            "user_id": getattr(request.state, "user_id", None),
        },
        exc_info=True,
    )
    # Return generic message to client
    return JSONResponse(
        status_code=500,
        content={
            "error": "An unexpected error occurred. Please try again later.",
            "request_id": getattr(request.state, "request_id", "unknown"),
        },
    )
```

---

## 3. Input Validation Patterns

### 3.1 Pydantic Models (Recommended)

```python
from pydantic import BaseModel, Field, EmailStr, field_validator
import re

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    name: str = Field(min_length=1, max_length=100)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not re.match(r"^[\w\s\-'.]+$", v, re.UNICODE):
            raise ValueError("Name contains invalid characters")
        return v.strip()

class UpdateProfileRequest(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    bio: str | None = Field(None, max_length=500)
    # CRITICAL: Never include role, is_admin, is_verified

# Usage in FastAPI endpoint
@router.post("/register")
async def register(data: RegisterRequest):
    # data is already validated by Pydantic
    hashed = await hash_password(data.password)
    user = await create_user(email=data.email, name=data.name, password_hash=hashed)
    return {"id": user.id}
```

### 3.2 Anti-patterns

```python
# BAD: No validation
@router.post("/users")
async def create_user(request: Request):
    body = await request.json()
    await db.users.insert_one(body)  # Mass assignment + no validation

# BAD: Denylist validation
if "<script>" in name:
    raise ValueError("Invalid name")

# BAD: Using raw dict when Pydantic model exists
@router.put("/profile")
async def update_profile(request: Request):
    body = await request.json()
    await db.users.update_one({"_id": user_id}, {"$set": body})  # Mass assignment
```

---

## 4. Authentication Implementation

### 4.1 Password Hashing with Argon2

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher(
    time_cost=3,        # 3 iterations
    memory_cost=65536,   # 64 MB
    parallelism=4,       # 4 threads
    hash_len=32,
    salt_len=16,
    type=argon2.Type.ID,  # Argon2id
)

def hash_password(plaintext: str) -> str:
    return ph.hash(plaintext)

def verify_password(plaintext: str, hashed: str) -> bool:
    try:
        return ph.verify(hashed, plaintext)
    except VerifyMismatchError:
        return False
```

### 4.2 JWT Implementation

```python
import jwt  # PyJWT
from datetime import datetime, timedelta, timezone

SECRET_KEY = os.environ["JWT_SECRET"]  # NEVER hardcode
ALGORITHM = "HS256"  # Or RS256 with key pair

def create_access_token(user_id: int, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15),  # Short-lived
        "iss": "https://api.example.com",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],  # CRITICAL: Explicit list, prevents 'none' attack
        options={
            "require": ["exp", "sub", "iss"],
            "verify_exp": True,
            "verify_iss": True,
        },
        issuer="https://api.example.com",
    )
```

### 4.3 Anti-patterns

```python
# BAD: No algorithm restriction
payload = jwt.decode(token, SECRET_KEY)  # Accepts ANY algorithm including 'none'

# BAD: Weak secret
SECRET_KEY = "secret"

# BAD: Long expiration
jwt.encode(payload, key, algorithm="HS256")  # No 'exp' claim at all

# BAD: Disabling verification
jwt.decode(token, options={"verify_signature": False})  # NEVER do this
```

---

## 5. Database Security

### 5.1 SQLAlchemy (Parameterized by Default)

```python
from sqlalchemy import select, text
from sqlalchemy.orm import Session

# GOOD: ORM queries — parameterized automatically
async def get_user_invoices(db: Session, user_id: int, invoice_id: int):
    stmt = select(Invoice).where(
        Invoice.id == invoice_id,
        Invoice.user_id == user_id,  # IDOR protection: ownership check
    )
    return db.execute(stmt).scalar_one_or_none()

# GOOD: Raw query with bound parameters (when ORM is insufficient)
result = db.execute(
    text("SELECT * FROM users WHERE email = :email"),
    {"email": user_email},
)

# BAD: String formatting in queries — SQL INJECTION
result = db.execute(text(f"SELECT * FROM users WHERE email = '{user_email}'"))

# BAD: Using .format() — SQL INJECTION
query = "SELECT * FROM users WHERE id = {}".format(user_id)
```

### 5.2 Django ORM

```python
# GOOD: Django ORM — parameterized by default
invoice = Invoice.objects.filter(id=invoice_id, user=request.user).first()

# GOOD: Raw query with params
User.objects.raw("SELECT * FROM auth_user WHERE email = %s", [email])

# BAD: String formatting — SQL INJECTION
User.objects.raw(f"SELECT * FROM auth_user WHERE email = '{email}'")

# BAD: extra() with unsanitized input
User.objects.extra(where=[f"email = '{email}'"])
```

---

## 6. Dangerous Functions to Audit

| Function | Risk | Mitigation |
|---|---|---|
| `eval()` | Code injection | Remove entirely. Use `ast.literal_eval()` for safe literal parsing only. |
| `exec()` | Code injection | Remove entirely. |
| `compile()` | Code injection | Avoid with user input. |
| `os.system()` | Command injection | Use `subprocess.run()` with argument list. |
| `subprocess.run(shell=True)` | Command injection | Use `shell=False` (default) with argument list. |
| `pickle.loads()` | Arbitrary code execution | Never unpickle untrusted data. Use JSON instead. |
| `yaml.load()` | Code execution | Use `yaml.safe_load()` always. |
| `__import__()` with variable | Arbitrary import | Never use user input in imports. |
| `open()` with user input | Path traversal | Validate path with `os.path.realpath()` + prefix check. |
| `random.random()` | Predictable | Use `secrets.token_bytes()` / `secrets.token_hex()`. |
| `hashlib.md5()` / `hashlib.sha1()` | Weak hash (for security) | Use `hashlib.sha256()` minimum. For passwords: argon2/bcrypt. |
| `tempfile.mktemp()` | Race condition | Use `tempfile.mkstemp()` or `tempfile.NamedTemporaryFile()`. |

---

## 7. Secure Random Generation

```python
import secrets
import uuid

# GOOD: Secure random token
token = secrets.token_hex(32)       # 64-character hex string
token = secrets.token_urlsafe(32)   # URL-safe base64 string

# GOOD: Secure random integer
code = secrets.randbelow(1000000)   # 6-digit OTP

# GOOD: Secure UUID
id = uuid.uuid4()

# GOOD: Timing-safe comparison
import hmac
is_valid = hmac.compare_digest(expected_token, provided_token)

# BAD: Predictable
import random
token = ''.join(random.choices('abcdef0123456789', k=32))  # NOT cryptographically secure
```

---

## 8. Logging Configuration (structlog)

```python
import structlog
import logging

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)

logger = structlog.get_logger()

# Usage
logger.info("auth.login.success", user_id=user.id, ip=request.client.host)
logger.warning("auth.login.failed", email=email, ip=request.client.host)
logger.error("unhandled.error", error=str(exc), request_id=request.state.request_id)

# CRITICAL: Never log sensitive data
# BAD: logger.info("login", password=password)
# BAD: logger.info("token issued", token=jwt_token)
```

---

## 9. File Upload Security

```python
import magic
import uuid
from pathlib import Path

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "application/pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
UPLOAD_DIR = Path("/var/uploads")  # OUTSIDE web root

async def handle_upload(file: UploadFile) -> str:
    # 1. Size check
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise ValueError("File too large")

    # 2. Magic byte check (NOT Content-Type header)
    detected_type = magic.from_buffer(contents, mime=True)
    if detected_type not in ALLOWED_TYPES:
        raise ValueError(f"File type not allowed: {detected_type}")

    # 3. Random filename (never use original)
    ext = Path(file.filename).suffix.lower() if file.filename else ""
    if ext not in {".jpg", ".jpeg", ".png", ".gif", ".pdf"}:
        ext = ".bin"
    safe_name = f"{uuid.uuid4()}{ext}"

    # 4. Store outside web root
    dest = UPLOAD_DIR / safe_name
    dest.write_bytes(contents)

    return safe_name
```

---

## 10. Path Traversal Prevention

```python
import os
from pathlib import Path

SAFE_BASE = Path("/var/app/data").resolve()

def safe_file_read(user_path: str) -> bytes:
    # Resolve to absolute path
    requested = (SAFE_BASE / user_path).resolve()

    # Verify it's still within the safe base
    if not str(requested).startswith(str(SAFE_BASE)):
        raise PermissionError("Path traversal detected")

    if not requested.is_file():
        raise FileNotFoundError("File not found")

    return requested.read_bytes()

# BAD: No path validation
def bad_file_read(user_path: str) -> bytes:
    return open(f"/var/app/data/{user_path}", "rb").read()  # ../../../etc/passwd
```

---

## 11. Environment & Configuration Security

```python
import os
import sys

REQUIRED_ENV = ["DATABASE_URL", "JWT_SECRET", "SECRET_KEY"]

def validate_environment():
    """Call at application startup. Fail fast if misconfigured."""
    missing = [key for key in REQUIRED_ENV if not os.environ.get(key)]
    if missing:
        print(f"FATAL: Missing required environment variables: {', '.join(missing)}")
        sys.exit(1)

    if os.environ.get("ENV") == "production":
        if os.environ.get("JWT_SECRET") == "development-secret":
            print("FATAL: Default JWT secret in production")
            sys.exit(1)
        if os.environ.get("DEBUG", "").lower() == "true":
            print("FATAL: DEBUG mode enabled in production")
            sys.exit(1)

validate_environment()
```
