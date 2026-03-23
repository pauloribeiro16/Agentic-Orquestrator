# Resolved Issues & Lessons Learned

> **Objective:** Avoid repeating past mistakes. Agents MUST append to this file after every successful debug cycle or critical fix.
> Check this file BEFORE proposing fixes for recurring symptoms.

---

| Date | Issue Symptom | Root Cause | Resolution / Fix | Prevention Rule |
|:---|:---|:---|:---|:---|
| `2026-03-23` | *Example: Database timeout on high load* | *Un-indexed query on `users.email` column* | *Added index via migration `idx_users_email`* | *Always verify indexing on `.find_by(X)` queries in Code Review* |

---

## 📖 How to Update This File

When a bug is resolved, insert a new row to the table above. 

### Format Guideline

1. **Date:** `YYYY-MM-DD`
2. **Issue Symptom:** What broke? (e.g., "Page crashes on refresh," "API returns 500 on auth headers")
3. **Root Cause:** *Why* did it break? (e.g., "Race condition in state load," "Null pointer on undefined token")
4. **Resolution / Fix:** What did we change? (e.g., "Added `.catch()` fallback," "Updated dependency XYZ")
5. **Prevention Rule:** Actionable advice for future agents (e.g., "Never chain promises without `.catch`").

---

## 🛠️ Active Remediation Logs

Use this space for deep-dive post-mortems if a bug required multi-step debugging.

### [YYYY-MM-DD] [Short Description]
- **Symptoms:** ...
- **Root Cause Analysis:** (The 5 Whys)
- **Fix Applied:** ...
- **Required Verification:** ...
