# Big Data Algorithms Homework  
_repo: goit-algo2-hw-05_

---
## ⚙️ Setup:

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---
## Task 1: Password Uniqueness with Bloom Filter 🔐 

**File:** `bloom_passwords.py`  

- Implement `BloomFilter(size, num_hashes)`  
- Function `check_password_uniqueness(bloom, passwords)` → reports "unique" or "already used" 

**Run:**

```bash
python bloom_passwords.py
```
---

## Task 2: Unique-IP Count Comparison (Exact vs HyperLogLog) 🌐
**File:** `hyperloglog_comparison.py`

-  Exact count via Python `set`
- Approximate count via `datasketch.HyperLogLog`
- Outputs a Markdown table of counts and timing

**Run:**

```bash
python hyperloglog_comparison.py
```
