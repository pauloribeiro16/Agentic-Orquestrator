---
description: "Knowledge Base — Node.js Security"
type: "reference"
scope: "stack-specific"
stack: "Node.js / JavaScript / TypeScript"
last_updated: "2025-01-01"
---

# Node.js Security

**Purpose:** Stack-specific secure coding guidance for Node.js applications. Covers recommended libraries, secure configuration patterns, and concrete anti-patterns with code examples.

---

## 1. Recommended Security Libraries

| Category | Library | Version | Purpose | Notes |
|---|---|---|---|---|
| **HTTP Security Headers** | `helmet` | 7.x | Sets secure HTTP headers in one line | Always use in Express/Fastify apps |
| **Rate Limiting** | `express-rate-limit` | 7.x | Brute force protection | Use with Redis store for distributed apps |
| **Rate Limit Store** | `rate-limit-redis` | 4.x | Redis-backed rate limit store | Required for multi-instance deployments |
| **Input Validation** | `zod` | 3.x | Schema validation with TypeScript inference | Preferred for TypeScript projects |
| **Input Validation** | `joi` | 17.x | Schema validation | Mature, widely adopted |
| **Password Hashing** | `bcrypt` | 5.x | bcrypt implementation | Use cost factor ≥ 10 |
| **Password Hashing** | `argon2` | 0.40.x | Argon2id implementation | Preferred over bcrypt for new projects |
| **JWT** | `jsonwebtoken` | 9.x | JWT sign/verify | Always specify algorithm explicitly |
| **JWT (faster)** | `jose` | 5.x | JOSE/JWT/JWE/JWS | Modern, standards-compliant, no native deps |
| **CSRF** | `csurf` (deprecated) | — | — | Use `SameSite` cookies + custom token instead |
| **CSRF** | `csrf-csrf` | 3.x | Double-submit CSRF protection | Modern replacement for csurf |
| **Sanitization** | `dompurify` + `jsdom` | 3.x | HTML sanitization (server-side) | For any user-submitted HTML |
| **Sanitization** | `sanitize-html` | 2.x | HTML sanitization | Simpler API, good for basic needs |
| **SQL ORM** | `prisma` | 5.x | Type-safe ORM | Parameterized by default |
| **SQL ORM** | `knex` | 3.x | Query builder | Use `.where()` methods, never raw concat |
| **MongoDB ODM** | `mongoose` | 8.x | MongoDB ODM | Use schema validation, sanitize `$` operators |
| **Logging** | `pino` | 8.x | Structured JSON logging | Fast, low overhead |
| **Logging** | `winston` | 3.x | Flexible logging | More features, slightly heavier |
| **Secrets** | `dotenv` | 16.x | Load .env files | Development only — use vault in production |
| **CORS** | `cors` | 2.x | CORS middleware | Always configure explicit origin allowlist |

---

## 2. Express.js Security Configuration

### 2.1 Essential Security Middleware Stack

```javascript
const express = require('express');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const cors = require('cors');

const app = express();

// 1. Security headers (ALWAYS first middleware)
app.use(helmet());
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"],  // No 'unsafe-inline' or 'unsafe-eval'
    styleSrc: ["'self'", "'unsafe-inline'"],  // CSS may need inline
    imgSrc: ["'self'", "data:", "https:"],
    connectSrc: ["'self'"],
    frameSrc: ["'none'"],
    objectSrc: ["'none'"],
  }
}));

// 2. CORS — explicit allowlist, NEVER wildcard for credentialed requests
app.use(cors({
  origin: ['https://app.example.com', 'https://admin.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  credentials: true,
  maxAge: 86400,
}));

// 3. Body parsing with size limits
app.use(express.json({ limit: '1mb' }));
app.use(express.urlencoded({ extended: false, limit: '1mb' }));

// 4. Global rate limiting
const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests, please try again later.' },
});
app.use(globalLimiter);

// 5. Aggressive rate limiting on auth endpoints
const authLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 20,  // 20 attempts per hour per IP
  skipSuccessfulRequests: true,
});
app.use('/api/auth/login', authLimiter);
app.use('/api/auth/register', authLimiter);
app.use('/api/auth/forgot-password', authLimiter);

// 6. Disable X-Powered-By (helmet does this, but being explicit)
app.disable('x-powered-by');
```

### 2.2 Global Error Handler

```javascript
// ALWAYS register this LAST, after all routes
app.use((err, req, res, next) => {
  // Log full error internally
  logger.error('Unhandled error', {
    error: err.message,
    stack: err.stack,
    method: req.method,
    path: req.path,
    correlationId: req.id,
    userId: req.user?.id,
  });

  // Return generic message to client
  const statusCode = err.statusCode || 500;
  res.status(statusCode).json({
    error: statusCode === 500
      ? 'An unexpected error occurred. Please try again later.'
      : err.message,
    correlationId: req.id,
  });
});

// Catch unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  logger.fatal('Unhandled Rejection', { reason });
  process.exit(1);
});

// Catch uncaught exceptions
process.on('uncaughtException', (error) => {
  logger.fatal('Uncaught Exception', { error: error.message, stack: error.stack });
  process.exit(1);
});
```

---

## 3. Input Validation Patterns

### 3.1 Zod Schema Validation (Recommended)

```javascript
const { z } = require('zod');

// Define schemas once, reuse everywhere
const registerSchema = z.object({
  email: z.string().email().max(255),
  password: z.string().min(12).max(128),
  name: z.string().min(1).max(100).regex(/^[\p{L}\p{N}\s\-'.]+$/u),
});

const updateProfileSchema = z.object({
  name: z.string().min(1).max(100).optional(),
  bio: z.string().max(500).optional(),
  // CRITICAL: Never include role, isAdmin, isVerified in user-facing schemas
});

// Validation middleware factory
function validate(schema) {
  return (req, res, next) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({
        error: 'Validation failed',
        details: result.error.issues.map(i => ({
          field: i.path.join('.'),
          message: i.message,
        })),
      });
    }
    req.validated = result.data;  // Use validated data, not raw req.body
    next();
  };
}

// Usage
router.post('/register', validate(registerSchema), authController.register);
router.put('/profile', authenticate, validate(updateProfileSchema), profileController.update);
```

### 3.2 Anti-patterns

```javascript
// BAD: No validation
app.post('/api/users', (req, res) => {
  User.create(req.body);  // Mass assignment + no validation
});

// BAD: Denylist validation
if (req.body.name.includes('<script>')) {
  return res.status(400).json({ error: 'Invalid name' });
}

// BAD: Client-side validation only
// (Frontend validates, but backend accepts anything)

// BAD: Validating but still using raw body
const result = schema.safeParse(req.body);
if (result.success) {
  User.create(req.body);  // Should use result.data, not req.body
}
```

---

## 4. Authentication Implementation

### 4.1 Password Hashing with Argon2id

```javascript
const argon2 = require('argon2');

// Hash password
async function hashPassword(plaintext) {
  return argon2.hash(plaintext, {
    type: argon2.argon2id,
    memoryCost: 65536,   // 64 MB
    timeCost: 3,          // 3 iterations
    parallelism: 4,       // 4 threads
  });
}

// Verify password
async function verifyPassword(plaintext, hash) {
  return argon2.verify(hash, plaintext);
}
```

### 4.2 Password Hashing with bcrypt

```javascript
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 12;  // Minimum 10, prefer 12+

async function hashPassword(plaintext) {
  return bcrypt.hash(plaintext, SALT_ROUNDS);
}

async function verifyPassword(plaintext, hash) {
  return bcrypt.compare(plaintext, hash);
}
```

### 4.3 JWT Implementation

```javascript
const jose = require('jose');

// GOOD: Asymmetric signing with explicit algorithm
const privateKey = await jose.importPKCS8(process.env.JWT_PRIVATE_KEY, 'RS256');
const publicKey = await jose.importSPKI(process.env.JWT_PUBLIC_KEY, 'RS256');

async function signToken(payload) {
  return new jose.SignJWT(payload)
    .setProtectedHeader({ alg: 'RS256' })
    .setIssuedAt()
    .setIssuer('https://api.example.com')
    .setAudience('https://app.example.com')
    .setExpirationTime('15m')  // Short-lived access tokens
    .sign(privateKey);
}

async function verifyToken(token) {
  const { payload } = await jose.jwtVerify(token, publicKey, {
    issuer: 'https://api.example.com',
    audience: 'https://app.example.com',
    algorithms: ['RS256'],  // Explicitly restrict algorithms
  });
  return payload;
}
```

### 4.4 JWT Anti-patterns

```javascript
// BAD: Weak secret
jwt.sign(payload, 'secret123', { algorithm: 'HS256' });

// BAD: No algorithm restriction (allows "none" attack)
jwt.verify(token, secret);

// BAD: Long expiration
jwt.sign(payload, secret, { expiresIn: '30d' });

// BAD: Sensitive data in payload
jwt.sign({ userId: 1, email: 'user@example.com', ssn: '123-45-6789' }, secret);

// BAD: Storing in localStorage (vulnerable to XSS)
localStorage.setItem('token', token);
```

---

## 5. Database Security

### 5.1 Parameterized Queries (Prisma)

```javascript
// GOOD: Prisma — parameterized by default
const user = await prisma.user.findUnique({ where: { id: userId } });
const invoices = await prisma.invoice.findMany({
  where: { userId: authenticatedUser.id },  // Ownership check
});

// DANGEROUS: Raw queries — only if absolutely necessary, still parameterized
const result = await prisma.$queryRaw`
  SELECT * FROM users WHERE email = ${email}
`;

// BAD: String interpolation in raw query
const result = await prisma.$queryRawUnsafe(
  `SELECT * FROM users WHERE email = '${email}'`  // SQL INJECTION
);
```

### 5.2 Parameterized Queries (Knex)

```javascript
// GOOD: Knex query builder — parameterized
const users = await knex('users').where('id', userId).first();
const invoices = await knex('invoices')
  .where('id', invoiceId)
  .andWhere('user_id', authenticatedUser.id);  // Ownership check

// BAD: Raw string concatenation
const users = await knex.raw(`SELECT * FROM users WHERE id = '${userId}'`);

// GOOD: Raw with bindings (when raw is necessary)
const users = await knex.raw('SELECT * FROM users WHERE id = ?', [userId]);
```

### 5.3 MongoDB Injection Prevention

```javascript
// BAD: Operator injection — attacker sends { "$gt": "" } as password
const user = await User.findOne({ email: req.body.email, password: req.body.password });

// GOOD: Explicitly cast/validate types
const email = String(req.body.email);
const password = String(req.body.password);

// GOOD: Use Zod to enforce types before querying
const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(12),
});
```

---

## 6. Cookie Security

```javascript
// Secure cookie configuration
app.use(session({
  name: '__Host-session',  // __Host- prefix for extra security
  secret: process.env.SESSION_SECRET,  // Strong, random secret from env
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,       // HTTPS only
    httpOnly: true,      // No JavaScript access
    sameSite: 'strict',  // No cross-site sending
    maxAge: 30 * 60 * 1000,  // 30 minutes
    path: '/',
    domain: undefined,   // Default to current domain only
  },
  store: new RedisStore({ client: redisClient }),  // NEVER use in-memory store in production
}));
```

---

## 7. Dangerous Functions to Audit

| Function | Risk | Mitigation |
|---|---|---|
| `eval()` | Code injection | Remove entirely. No exceptions. |
| `Function()` constructor | Code injection | Remove entirely. |
| `setTimeout(string)` | Code injection | Use function reference: `setTimeout(fn, ms)` |
| `setInterval(string)` | Code injection | Use function reference. |
| `child_process.exec()` | Command injection | Use `execFile()` with argument array instead. |
| `child_process.spawn({ shell: true })` | Command injection | Use `spawn()` without shell option. |
| `vm.runInContext()` | Sandbox escape | Use `vm2` or `isolated-vm` if sandboxing is needed. |
| `require()` with variable | LFI / arbitrary code execution | Never use user input in `require()`. |
| `fs.readFile()` with user input | Path traversal | Validate path, use `path.resolve()` + `startsWith()` check. |
| `dangerouslySetInnerHTML` | XSS | Sanitize with DOMPurify before rendering. |
| `Math.random()` | Predictable randomness | Use `crypto.randomBytes()` or `crypto.randomUUID()`. |
| `Buffer.allocUnsafe()` | Info disclosure | Use `Buffer.alloc()` (zero-filled). |

---

## 8. Secure Random Generation

```javascript
const crypto = require('crypto');

// GOOD: Secure random token
function generateToken(bytes = 32) {
  return crypto.randomBytes(bytes).toString('hex');
}

// GOOD: Secure random UUID
function generateId() {
  return crypto.randomUUID();
}

// GOOD: Timing-safe comparison
function safeCompare(a, b) {
  if (a.length !== b.length) return false;
  return crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b));
}

// BAD: Predictable
const token = Math.random().toString(36).substring(2);
```

---

## 9. Logging Configuration (Pino)

```javascript
const pino = require('pino');

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  timestamp: pino.stdTimeFunctions.isoTime,
  // Redact sensitive fields automatically
  redact: {
    paths: [
      'req.headers.authorization',
      'req.headers.cookie',
      'password',
      'token',
      'secret',
      'creditCard',
      'ssn',
    ],
    censor: '[REDACTED]',
  },
  // Structured format for SIEM
  formatters: {
    level: (label) => ({ level: label }),
  },
});

// Usage
logger.info({ event: 'auth.login.success', userId: user.id, ip: req.ip });
logger.warn({ event: 'auth.login.failed', email: req.body.email, ip: req.ip });
logger.error({ event: 'unhandled.error', error: err.message, correlationId: req.id });
```

---

## 10. Environment & Configuration Security

```javascript
// CRITICAL: Validate required environment variables at startup
const required = ['DATABASE_URL', 'JWT_SECRET', 'SESSION_SECRET', 'NODE_ENV'];
for (const key of required) {
  if (!process.env[key]) {
    console.error(`FATAL: Missing required environment variable: ${key}`);
    process.exit(1);
  }
}

// CRITICAL: Ensure production settings
if (process.env.NODE_ENV === 'production') {
  if (process.env.JWT_SECRET === 'development-secret') {
    console.error('FATAL: Default JWT secret detected in production');
    process.exit(1);
  }
}
```
