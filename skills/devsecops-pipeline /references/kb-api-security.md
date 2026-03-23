---
description: "Knowledge Base — API Security"
type: "reference"
scope: "feature-conditional"
stack: "Node.js, Python"
last_updated: "2025-01-01"
---

# API Security

**Purpose:** Security guidance for designing and building secure REST and GraphQL APIs. Loaded when the feature exposes API endpoints.

---

## 1. API Authentication Patterns

### 1.1 Token-Based (Recommended for SPAs and Mobile)
- Use short-lived JWTs (access tokens: 5–15 min) with refresh token rotation.
- Access tokens in `Authorization: Bearer <token>` header.
- Refresh tokens in HttpOnly, Secure, SameSite cookies — NOT in localStorage.
- On refresh, issue a new refresh token and invalidate the old one (rotation).

### 1.2 Cookie-Based (For Server-Rendered + Same-Origin)
- Session ID in HttpOnly, Secure, SameSite=Strict cookie.
- Server-side session storage (Redis, database) — never in-memory in production.
- CSRF protection mandatory on all state-changing endpoints (POST, PUT, DELETE).

### 1.3 API Key (For Server-to-Server Only)
- API keys for machine-to-machine authentication only — never for end-user auth.
- Keys sent in a custom header (`X-API-Key`), never in query parameters.
- Keys scoped to specific permissions and rotatable.

### 1.4 Anti-patterns
- Tokens in URL query strings (logged, cached, exposed in Referer header).
- API keys as the sole authentication for user-facing endpoints.
- Bearer tokens in localStorage (accessible to any XSS).
- Long-lived tokens without refresh mechanism (30-day JWTs).

---

## 2. API Authorization Patterns

### 2.1 Route-Level + Resource-Level (Defense in Depth)

```javascript
// Layer 1: Route-level middleware — checks role/permission
router.get('/api/invoices/:id',
  authenticate,                    // Verify identity
  authorize('read:invoices'),       // Verify permission
  invoiceController.getById         // Business logic
);

// Layer 2: Resource-level check — verifies ownership in the query
async getById(req, res) {
  const invoice = await Invoice.findOne({
    id: req.params.id,
    userId: req.user.id,  // Ownership check — prevents IDOR
  });
  if (!invoice) return res.status(404).json({ error: 'Not found' });
  return res.json(invoice);
}
```

### 2.2 DTO Pattern (Response Filtering)

Never return raw database objects. Use explicit response shapes.

```javascript
// BAD: Returns everything including internal fields
res.json(user);  // { id, email, passwordHash, role, internalNotes, createdAt, ... }

// GOOD: Explicit DTO
const userResponse = {
  id: user.id,
  email: user.email,
  name: user.name,
  createdAt: user.createdAt,
};
res.json(userResponse);
```

```python
# GOOD: Pydantic response model
class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("/users/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    return user  # Pydantic strips fields not in UserResponse
```

### 2.3 Mass Assignment Prevention

```javascript
// BAD: Accept any fields from client
const user = await User.create(req.body);

// GOOD: Explicit allowlist
const { name, email, bio } = req.validated;  // From Zod-validated data
const user = await User.create({ name, email, bio });
```

---

## 3. Input Validation for APIs

### 3.1 Content-Type Enforcement

```javascript
// Middleware: Reject unexpected Content-Types
app.use('/api', (req, res, next) => {
  if (['POST', 'PUT', 'PATCH'].includes(req.method)) {
    const contentType = req.headers['content-type'];
    if (!contentType || !contentType.includes('application/json')) {
      return res.status(415).json({ error: 'Unsupported Media Type. Use application/json.' });
    }
  }
  next();
});
```

### 3.2 Payload Size Limits

```javascript
// Express
app.use(express.json({ limit: '1mb' }));
app.use(express.urlencoded({ limit: '1mb', extended: false }));

// FastAPI
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

MAX_BODY_SIZE = 1 * 1024 * 1024  # 1 MB

class LimitBodySizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > MAX_BODY_SIZE:
            return JSONResponse(status_code=413, content={"error": "Payload too large"})
        return await call_next(request)
```

### 3.3 Pagination (Mandatory on List Endpoints)

```javascript
// GOOD: Enforced pagination with reasonable limits
const page = Math.max(1, parseInt(req.query.page) || 1);
const limit = Math.min(100, Math.max(1, parseInt(req.query.limit) || 20));
const offset = (page - 1) * limit;

const items = await Item.findAll({ limit, offset, where: { userId: req.user.id } });
const total = await Item.count({ where: { userId: req.user.id } });

res.json({
  data: items,
  pagination: { page, limit, total, pages: Math.ceil(total / limit) },
});

// BAD: No pagination — full table dump
const items = await Item.findAll();
```

---

## 4. Rate Limiting Strategy

### 4.1 Tiered Rate Limiting

| Endpoint Category | Rate Limit | Window | Key |
|---|---|---|---|
| Authentication (login, register, forgot-password) | 20 requests | 1 hour | IP address |
| Authenticated API endpoints | 100 requests | 15 minutes | User ID |
| Public API endpoints | 60 requests | 15 minutes | IP address |
| File upload | 10 requests | 1 hour | User ID |
| Password change | 5 requests | 1 hour | User ID |
| Admin endpoints | 200 requests | 15 minutes | User ID |

### 4.2 Implementation

```javascript
// Express with express-rate-limit
const rateLimit = require('express-rate-limit');

const authLimiter = rateLimit({
  windowMs: 60 * 60 * 1000,
  max: 20,
  keyGenerator: (req) => req.ip,
  skipSuccessfulRequests: true,
  standardHeaders: true,
  message: { error: 'Too many attempts. Please try again later.' },
});

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  keyGenerator: (req) => req.user?.id || req.ip,
  standardHeaders: true,
});

app.use('/api/auth', authLimiter);
app.use('/api', authenticate, apiLimiter);
```

---

## 5. GraphQL Security

### 5.1 Query Depth Limiting

```javascript
const depthLimit = require('graphql-depth-limit');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimit(5)],  // Max 5 levels deep
});
```

### 5.2 Query Complexity Limiting

```javascript
const { createComplexityLimitRule } = require('graphql-validation-complexity');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    createComplexityLimitRule(1000, {
      scalarCost: 1,
      objectCost: 10,
      listFactor: 20,
    }),
  ],
});
```

### 5.3 Disable Introspection in Production

```javascript
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production',
});
```

### 5.4 Batching Attack Prevention
Rate limit per operation, not per HTTP request:

```javascript
// If using Apollo: limit batch size
const server = new ApolloServer({
  allowBatchedHttpRequests: false,  // Disable batching entirely
  // OR limit: maxBatchSize: 5
});
```

---

## 6. CORS Configuration

### 6.1 Secure Configuration

```javascript
// GOOD: Strict allowlist
app.use(cors({
  origin: (origin, callback) => {
    const allowed = ['https://app.example.com', 'https://admin.example.com'];
    if (!origin || allowed.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 86400,
}));
```

### 6.2 Anti-patterns

```javascript
// BAD: Wildcard with credentials
app.use(cors({ origin: '*', credentials: true }));

// BAD: Dynamically echo origin without validation
app.use(cors({
  origin: (origin, callback) => callback(null, origin),  // Reflects ANY origin
}));

// BAD: Allowing null origin
app.use(cors({ origin: [null, 'https://app.example.com'] }));
```

---

## 7. API Error Response Standards

### 7.1 Standard Error Shape

```json
{
  "error": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": [
    { "field": "email", "message": "Must be a valid email address" },
    { "field": "password", "message": "Must be at least 12 characters" }
  ],
  "requestId": "req-abc-123"
}
```

### 7.2 Status Code Usage

| Code | Meaning | When to Use |
|---|---|---|
| 400 | Bad Request | Validation errors, malformed input |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but insufficient permissions |
| 404 | Not Found | Resource doesn't exist OR user doesn't have access (avoids info disclosure) |
| 405 | Method Not Allowed | Wrong HTTP method |
| 409 | Conflict | Duplicate resource (e.g., email already registered) |
| 413 | Payload Too Large | Body exceeds size limit |
| 415 | Unsupported Media Type | Wrong Content-Type |
| 422 | Unprocessable Entity | Valid JSON but fails business logic validation |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unhandled exception — ALWAYS generic message |

### 7.3 Account Enumeration Prevention
For login and registration, use identical responses for all failure cases:

```javascript
// Login — same response whether email exists or not
res.status(401).json({ error: 'Invalid email or password.' });

// Registration — same response whether email is taken or not
res.status(200).json({ message: 'If this email is valid, a verification link has been sent.' });

// Password reset — same response always
res.status(200).json({ message: 'If this email is registered, a reset link has been sent.' });
```

---

## 8. SSRF Prevention

```javascript
// GOOD: Domain allowlist for outbound requests
const ALLOWED_DOMAINS = new Set(['api.stripe.com', 'api.sendgrid.com', 'hooks.slack.com']);

function isAllowedUrl(urlString) {
  try {
    const url = new URL(urlString);
    // Block private IPs
    const hostname = url.hostname;
    if (hostname === 'localhost' || hostname === '127.0.0.1' ||
        hostname.startsWith('10.') || hostname.startsWith('172.') ||
        hostname.startsWith('192.168.') || hostname === '169.254.169.254' ||
        hostname === '0.0.0.0' || hostname === '::1') {
      return false;
    }
    // Check allowlist
    return ALLOWED_DOMAINS.has(url.hostname);
  } catch {
    return false;
  }
}
```

---

## 9. API Versioning Security
- Maintain security patches across all supported API versions.
- Deprecate and sunset old versions with documented timelines.
- Don't expose internal/debug API versions in production.
- Version in URL path (`/api/v1/`) or header (`Accept: application/vnd.api.v1+json`).
