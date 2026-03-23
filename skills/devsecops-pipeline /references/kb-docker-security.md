---
description: "Knowledge Base — Docker & Docker Compose Security"
type: "reference"
scope: "infrastructure"
stack: "Docker, Docker Compose, Containerization"
last_updated: "2026-03-10"
---

# Docker & Docker Compose Security Best Practices

**Purpose:** Comprehensive security guidance for building, running, and orchestrating secure Docker containers, with a heavy emphasis on Docker Compose configurations. Loaded when the project involves containerization, Dockerfiles, or local/production orchestration.

---

## 1. Image Building Patterns (Dockerfile)

### 1.1 Base Image Selection & Pinning
- **Always** use minimal base images (`alpine`, `distroless`, or `<lang>-slim`).
- **Never** use the `latest` tag in production. Mutable tags can break builds and introduce sudden vulnerabilities.
- **Pin to explicit SHAs** for deterministic and cryptographically guaranteed builds.

```dockerfile
# DANGEROUS: High attack surface, unpinned, unpredictable
FROM ubuntu:latest

# BETTER: Pinned to semantic version and slim variant
FROM python:3.11.7-slim-bookworm

# BEST: Pinned to immutable SHA256 digest
FROM clojure@sha256:1a2b3c4d5e6f7g8h9i0j...
```

### 1.2 Multi-Stage Builds (Attack Surface Reduction)
Compilers, headers, and build tools are security risks if left in the final image. Always use multi-stage builds so the final image only contains the compiled binary or final runtime files.

```dockerfile
# GOOD: Multi-stage build for a Node app
# Stage 1: Build & Prune
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
RUN npm prune --production # Removes devDependencies

# Stage 2: Production Runtime
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/build ./build
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "build/index.js"]
```

### 1.3 Secure Caching of Credentials
Never hardcode credentials like NPM tokens or SSH keys in a `ENV` or `ARG` line, as they will be permanently baked into the image history (`docker history`).

```dockerfile
# BAD: Token is visible in image layers forever
ARG NPM_TOKEN
RUN echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > .npmrc && \
    npm install

# GOOD: Docker BuildKit Secrets (Leaves no trace in the final image)
# Run with: docker build --secret id=npm_token,src=.npm_token .
RUN --mount=type=secret,id=npm_token \
    export NPM_TOKEN=$(cat /run/secrets/npm_token) && \
    echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > .npmrc && \
    npm ci && rm .npmrc
```

---

## 2. Docker Compose: Least Privilege & Capabilities

### 2.1 Never Run as Root
By default, Docker runs processes as `root` (UID 0). An attacker who achieves Remote Code Execution (RCE) inside the container is `root`. You must drop this.

**In the Dockerfile:**
```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

**In `docker-compose.yml` (Enforcement):**
```yaml
services:
  web:
    image: myapp:1.0
    user: "1000:1000"  # Enforces a specific non-root UID:GID at runtime
```

### 2.2 Drop Linux Capabilities
Linux uses "capabilities" to break down root privileges into smaller pieces. Docker grants 14 default capabilities (like `CHOWN`, `SETUID`, `NET_BIND_SERVICE`). Most web apps need **zero** capabilities.

```yaml
# GOOD: Drop all caps in Compose
services:
  api:
    image: myapi:1.0
    cap_drop:
      - ALL
    # If the app binds to port 80 (requires root privilege usually), add it back:
    # cap_add:
    #   - NET_BIND_SERVICE 
```

### 2.3 Prevent Privilege Escalation (no-new-privileges)
Even if you run as a non-root user, a binary with the `SUID` bit set inside the container could allow the process to escalate back to root. Prevent this at the container level.

```yaml
# GOOD: Block privilege escalation
services:
  database:
    image: postgres:15-alpine
    security_opt:
      - no-new-privileges:true
```

---

## 3. Docker Compose: File System Security

### 3.1 Read-Only Root Filesystem
If an attacker compromises your app, they will likely try to download a reverse shell or modify scripts (`wget http://malware | bash`). Make the entire container filesystem read-only to stop this.

```yaml
# BEST: Immutable container runtime
services:
  frontend:
    image: nginx:alpine
    read_only: true
    # Provide highly specific, temporary file systems for necessary writes
    tmpfs:
      - /tmp
      - /var/cache/nginx
      - /var/run
```

### 3.2 Volume Mount Permissions
When mounting volumes, ensure the container cannot maliciously alter host data unless explicitly required.

```yaml
services:
  monitoring:
    image: prometheus:latest
    volumes:
      # Use :ro (read-only) flag to protect host files
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - /etc/hostname:/etc/hostname:ro
```

---

## 4. Docker Compose: Secrets Management

### 4.1 The `.env` Anti-Pattern
Placing database passwords and API keys in a `.env` file and utilizing `env_file: .env` is historically common but dangerous if the container can be queried (e.g. Server Side Request Forgery) or if a process dumps environment variables on crash.

### 4.2 Docker Secrets (The Right Way)
Use Docker Compose's integrated `secrets` mechanism, which maps the secret to a secure, in-memory (`tmpfs`) file at `/run/secrets/`.

```yaml
# GOOD: Docker Compose Secrets implementation
services:
  db:
    image: postgres:15-alpine
    environment:
      # Postgres specifically supports _FILE suffixes to read from secrets
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

  web:
    image: myapp:1.0
    secrets:
      - db_password
    # The app code must read from fs.readFileSync('/run/secrets/db_password')

secrets:
  db_password:
    file: ./secrets/db_password.txt  # Must be excluded from git via .gitignore
```

---

## 5. Docker Compose: Network Security

### 5.1 Custom Network Isolation
Do not use the default `bridge` network. All containers on the default bridge can communicate. Explicitly define networks and map containers strictly to the networks they require.

```yaml
# BEST: Micro-segmentation in Compose
services:
  public-proxy:
    image: traefik:v2.10
    ports:
      - "443:443"
    networks:
      - frontend_net

  app-backend:
    image: myapp:1.0
    networks:
      - frontend_net  # Talks to proxy
      - backend_net   # Talks to DB

  database:
    image: postgres:15
    networks:
      - backend_net   # Proxy cannot reach DB organically

networks:
  frontend_net:
    driver: bridge
  backend_net:
    driver: bridge
```

### 5.2 Avoid Binding to `0.0.0.0` Unnecessarily
If an internal service (like Redis or Postgres) is only meant to be accessed by the backend container, **do not expose its ports to the host.**

```yaml
services:
  redis:
    image: redis:7-alpine
    # BAD: Exposes Redis directly to your laptop's network (or the public internet on a server)
    # ports:
    #   - "6379:6379"  
    
    # GOOD: Container remains hidden. The backend container can still reach it via http://redis:6379 on the internal Docker network.
```

If you *must* access it from the host machine for debugging, bind it strictly to localhost `127.0.0.1`.
```yaml
    ports:
      - "127.0.0.1:6379:6379"
```

---

## 6. Host & Resource Protection (DoS Defense)

### 6.1 Resource Constraints
If an app has a memory leak, or an attacker finds a compute-heavy endpoint, an unbounded container can crash the entire host OS by consuming 100% of RAM/CPU.

```yaml
# GOOD: Hard limits in Compose
services:
  api:
    image: myapi:1.0
    deploy:
      resources:
        limits:
          cpus: '0.50'        # Hard cap: Max 50% of one CPU core
          memory: 512M        # Hard cap: Docker kills container if it exceeds 512MB (OOM)
        reservations:
          cpus: '0.10'        # Guaranteed allocation minimum
          memory: 256M
```

### 6.2 PIDs Limit
Prevent Fork Bomb attacks by limiting the number of processes a container can spawn.

```yaml
services:
  web:
    image: nginx
    deploy:
      resources:
        pids: 100  # Container cannot spawn more than 100 processes
```

### 6.3 Restart Policies
Use deliberate restart policies to handle crashes gracefully, but prevent endless boot-loop resource exhaustion.

```yaml
services:
  api:
    image: myapi:1.0
    # BAD: restart: always (will loop forever if naturally broken)
    # GOOD:
    restart: on-failure:5
```

---

## 7. Operational & Orchestration Security

### 7.1 Mandatory Healthchecks
Docker needs to know if your app is actually healthy, not just if the process ID is running. Without a healthcheck, load balancers might route traffic to a dead/hanging application.

```yaml
services:
  api:
    image: myapp:1.0
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### 7.2 Secure Logging configuration
By default, Docker uses the `json-file` driver with unbounded size, meaning container logs can eventually fill the entire host disk (a common DoS vector).

```yaml
services:
  web:
    image: myapp:1.0
    logging:
      driver: "json-file"
      options:
        max-size: "20m"   # Rotate when file hits 20MB
        max-file: "3"     # Keep a maximum of 3 files
```

### 7.3 NEVER Mount the Docker Socket
Mounting the Docker socket inside a container is functionally equivalent to giving the container root access to the entire host machine. An attacker who breaches the container can simply run `docker run -v /:/host -it ubuntu bash` and own the host.

```yaml
# CATASTROPHIC RISK: Do not copy this pattern unless building core infra
services:
  ci-cd-agent:
    image: some-ci-tool
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock  # Extreme Danger
```
*Mitigation:* Use Docker-in-Docker (DinD) without privileged mode, or rootless Sysbox contexts for CI runners.

---

## 8. Summary: The Golden `docker-compose.yml` Pattern

This template combines all best practices into a single, highly secure default block.

```yaml
version: '3.8'

services:
  secure-app:
    image: myorganization/app:1.2.3@sha256:abcd...
    user: "1000:1000"
    restart: on-failure:5
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    networks:
      - isolated_backend
    secrets:
      - db_password
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        pids: 50
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/ping"]
      interval: 30s
      timeout: 5s
      retries: 3

networks:
  isolated_backend:
    driver: bridge

secrets:
  db_password:
    file: ./secrets/db_password.txt
```
