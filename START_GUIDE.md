
---

# ✅ Your Gunicorn Script Explained

```bash
#!/bin/bash

echo "Starting Flask API with Gunicorn..."

source venv/bin/activate

exec gunicorn app:app \
    --workers 2 \
    --bind 0.0.0.0:8000 \
    --timeout 120
```

### What this means:

| Option                | Meaning                       |
| --------------------- | ----------------------------- |
| `app:app`             | file `app.py`, variable `app` |
| `--workers 2`         | 2 Flask processes             |
| `--bind 0.0.0.0:8000` | accessible on port 8000       |
| `--timeout 120`       | request timeout 120 seconds   |

---

# 🧠 Important Concept

Gunicorn handles:

👉 **HTTP requests**

Celery handles:

👉 **Background tasks**

Redis handles:

👉 **Queue storage**

They are separate processes.

---

# 🏗️ Final Production Flow (With Gunicorn)

```
Client
   ↓
Gunicorn (2 workers)
   ↓
Flask App
   ↓
Celery
   ↓
Redis Queue
   ↓
Celery Worker (10 concurrency)
   ↓
LLM APIs
```

---

# 🚀 How To Run Everything Now (With Gunicorn)

Open **4 terminals**

---

## 🖥️ Terminal 1 — Start Redis

```bash
sudo service redis-server start
sudo service redis-server stop # To stop Redis when done

or 

redis-server # to stop just ctrl+c in that terminal
```

Verify:

```bash
redis-cli ping
```

Should return:

```
PONG
```

---

## 🖥️ Terminal 2 — Start Celery Worker

```bash
source venv/bin/activate
bash queuing/run_worker.sh
```

You should see:

```
Connected to redis://localhost:6379/0
Ready.
```

---

## 🖥️ Terminal 3 — Start Gunicorn

Make script executable:

```bash
chmod +x run_api.sh
```

Run:

```bash
source venv/bin/activate
./run_api.sh
```

Server now running on:

http://localhost:8000
---

## 🖥️ Terminal 4 — Start Flower

```bash
source venv/bin/activate
bash queuing/run_flower.sh
```

Open:

```
http://localhost:5555
```

---

# 📦 Now Send 30 Requests

```bash
python send_requests.py
```

---

# 🔍 What You Will See

### In Flower:

* Active → max 10 tasks
* Tasks → SUCCESS / STARTED / FAILURE
* Workers → shows concurrency

---

# 🔥 To See Queue Size (Very Important)

Open Redis CLI:

```bash
redis-cli
```

Check queue:

```bash
LLEN celery
```

If it shows:

```
(integer) 20
```

That means:

* 10 running
* 20 waiting
* 0 finished

---


# ⚙️ Recommended Production Improvements

## 1️⃣ Increase Gunicorn Workers Properly

Rule of thumb:

```
workers = (2 × CPU cores) + 1
```

Check CPU cores:

```bash
nproc
```

Example (4 cores):

```
(2 × 4) + 1 = 9 workers
```

---

## 2️⃣ Add Logging

Update script:

```bash
exec gunicorn app:app \
    --workers 2 \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log
```

---

## 3️⃣ Prevent Blocking

Since tasks are async (Celery):

Gunicorn workers only enqueue tasks → very fast.

So 2 workers is usually fine.

---

# 📊 Monitoring Summary

| Component       | How To Monitor            |
| --------------- | ------------------------- |
| Gunicorn        | Terminal logs             |
| Celery Worker   | Worker terminal           |
| Queue Size      | `redis-cli → LLEN celery` |
| Running Tasks   | Flower → Active           |
| Completed Tasks | Flower → SUCCESS          |

---

# 🏁 Final Confirmation

If:

* Gunicorn running on 8000
* Worker running with concurrency=10
* Redis running
* Flower running
* You send 30 requests
* Only 10 run at once
* Queue shows remaining
* Tasks finish gradually

Then your system is:

✅ Production-ready async backend
✅ Properly rate-limited
✅ Scalable
✅ Architecturally correct

---
