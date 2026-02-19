
---

# 🚀 AI Startup Report Generation System

### Flask + Gunicorn + Celery + Redis + LLM APIs

---

## 📌 Project Overview

This system generates **research-based startup reports** asynchronously for VC users.

Because report generation:

* Uses multiple external LLM APIs (OpenAI, Anthropic, Gemini)
* Makes multi-step research calls
* Is long-running (30–60 seconds per task)
* Is I/O heavy and rate-limit sensitive

We implemented:

* ✅ Asynchronous background processing (Celery)
* ✅ Controlled concurrency
* ✅ Redis as broker + result backend
* ✅ Retry with exponential backoff
* ✅ Flower monitoring dashboard
* ✅ Production-ready Gunicorn API server

---

# 🏗️ System Architecture

```
User
  ↓
Gunicorn (Flask API)
  ↓
Redis (Broker DB 0)
  ↓
Celery Worker (Concurrency = 4)
  ↓
External LLM APIs
  ↓
Redis (Result Backend DB 1)
  ↓
User checks task status
```

---

# 📂 Project Structure

```
task_queue/
│
├── app.py
├── send_requests.py
├── run_api.sh
├── requirements.txt
│
├── queuing/
│   ├── __init__.py
│   ├── celery_worker.py
│   ├── tasks.py
│   ├── run_worker.sh
│   └── run_flower.sh
│
└── venv/
```

---

# 🧠 Why This Architecture?

## Why Gunicorn?

Flask dev server:

* Single process
* Not production safe
* No process management

Gunicorn:

* Multiple workers
* Handles crashes
* Production-ready
* Scalable

---

## Why Celery?

Because:

* Report generation is long-running
* Needs retry handling
* Must control concurrency
* Must prevent API flooding

Celery provides:

* Distributed task execution
* Retry + backoff
* Concurrency control
* Task monitoring

---

## Why Redis?

Redis acts as:

* Message broker (DB 0)
* Result backend (DB 1)
* Fast in-memory queue
* Lightweight and reliable

---

# ⚙️ Concurrency Design (2 CPU / 4GB RAM)

### Gunicorn

```
--workers 2
--threads 2
```

### Celery Worker

```
--concurrency=4
--prefetch-multiplier=1
--max-tasks-per-child=20
```

Why 4?

* Tasks are I/O heavy (LLM calls)
* Not CPU bound
* Prevents memory exhaustion
* Safe for 2 CPU machine

---

# 🛠 Installation Guide (WSL / Ubuntu)

## 1️⃣ Install Redis

```bash
sudo apt update
sudo apt install redis-server
```

Start Redis:

```bash
sudo service redis-server start
```

Check:

```bash
redis-cli ping
```

Output:

```
PONG
```

---

## 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🚀 Running The System (Development)

---

## 1️⃣ Start Redis

```bash
sudo service redis-server start
sudo service redis-server stop # To stop Redis when done

```

---

## 2️⃣ Start Celery Worker

```bash
bash queuing/run_worker.sh
```

This runs:

```bash
celery -A queuing.celery_worker.celery_app worker \
    --loglevel=info \
    --concurrency=4 \
    --prefetch-multiplier=1 \
    --max-tasks-per-child=20 \
    -E
```

---

## 3️⃣ Start API (Gunicorn)

```bash
bash run_api.sh
```

This runs:

```bash
gunicorn app:app \
    --workers 2 \
    --threads 2 \
    --bind 0.0.0.0:8000 \
    --timeout 120
```

API available at:

```
http://localhost:8000
```

---

## 4️⃣ Start Flower (Optional)

```bash
bash queuing/run_flower.sh
```

Open:

```
http://localhost:5555
```

---

# 📦 Sending Bulk Tasks

Update `send_requests.py`:

```python
URL = "http://127.0.0.1:8000/generate"
```

Then run:

```bash
python send_requests.py
```

This sends 30 concurrent tasks.

Celery will:

* Execute 4 at a time
* Queue remaining
* Retry failures automatically

---

# 📊 Monitoring With Flower

Flower shows:

* Active tasks
* Completed tasks
* Failed tasks
* Worker health
* Queue backlog

Command:

```bash
celery -A queuing.celery_worker.celery_app flower --port=5555
```

---

# 🔁 Failure & Retry Strategy

Configured in task:

```python
autoretry_for=(Exception,)
retry_kwargs={"max_retries": 3}
retry_backoff=True
retry_backoff_max=300
```

Strategy:

* Retry up to 3 times
* Exponential backoff
* Prevent API flooding
* Handles timeouts and rate limits

---

# 📈 Scaling Strategy

## Vertical Scaling (Single Machine)

Increase:

```
--concurrency=6
--workers=3
```

Only if memory allows.

---

## Horizontal Scaling

Run multiple worker instances:

```
Machine A → 4 workers
Machine B → 4 workers
Machine C → 4 workers
```

All connected to SAME Redis.

Redis acts as centralized broker.

More workers = more throughput.

---

# ⚠️ Edge Cases Handled

| Scenario           | Solution            |
| ------------------ | ------------------- |
| LLM timeout        | Auto retry          |
| Worker crash       | Tasks re-queued     |
| Redis restart      | Worker reconnect    |
| High traffic spike | Queue backlog       |
| Memory leak        | max-tasks-per-child |

---

# 🔒 Production Improvements

Future enhancements:

* Nginx reverse proxy
* Redis persistence (AOF)
* systemd for auto-start
* Rate limiting middleware
* Authentication layer
* Store results in PostgreSQL
* Docker deployment
* Kubernetes scaling

---

# 🧪 API Usage

## Generate Report

```
POST /generate
{
  "startup": "TeslaAI"
}
```

Response:

```
{
  "job_id": "abc123",
  "status": "queued"
}
```

---

## Check Status

```
GET /status/<job_id>
```

Response:

```
{
  "job_id": "abc123",
  "state": "SUCCESS",
  "result": "Generated report..."
}
```

---

# 🧠 Why This Architecture Works

* API remains fast (non-blocking)
* Background processing handles heavy work
* Concurrency is controlled
* LLM usage is safe
* System is horizontally scalable
* Production-ready design

---

# 🏁 Conclusion

This project demonstrates:

* Distributed task queue design
* Production-grade Flask deployment with Gunicorn
* Celery concurrency control
* LLM orchestration architecture
* Monitoring & retry strategy
* Scalable backend design

It is suitable for AI-powered research automation platforms handling 50–100 concurrent users safely on a 2 CPU / 4GB machine.

---
