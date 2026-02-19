
---

# 🚀 AI Startup Report Generation System

### Flask + Celery + Redis + OpenAI/Anthropic/Gemini

---

## 📌 Project Overview

This system generates **detailed research-based startup reports** for Venture Capital (VC) users.

Because report generation:

* Uses multiple external LLM APIs (OpenAI, Anthropic, Gemini)
* Makes multiple research API calls
* Is compute & API intensive

We implemented:

* ✅ Asynchronous task processing
* ✅ Concurrency control (max 10 workers)
* ✅ Queue management using Redis
* ✅ Monitoring with Flower
* ✅ Metrics logging
* ✅ Bulk task handling

This ensures:

* System stability
* Controlled API usage
* No overload of external LLM providers
* Scalable architecture

---

# 🏗️ System Architecture

```
User Request
     ↓
Flask API (app.py)
     ↓
Celery Task Queue
     ↓
Redis (Broker + Result Backend)
     ↓
Celery Worker (Concurrency = 10)
     ↓
External LLM APIs
(OpenAI / Anthropic / Gemini)
     ↓
Generated Report Stored in Redis
     ↓
User Fetches Result
```

---

# 📂 Project Structure

```
TASK-QUEUE/
│
├── app.py              # Flask API server
├── celery_worker.py    # Celery configuration
├── tasks.py            # Report generation task
├── send_requests.py    # Script to send 30 tasks at once
├── start_worker.sh     # Worker startup script
├── start_flower.sh     # Flower dashboard script
├── requirements.txt
├── README.md
└── venv/
```

---

# 🧠 Why Celery + Redis?

## Why Celery?

Because:

* Report generation is long-running
* Multiple API calls per request
* Need concurrency control
* Need retry mechanisms

Celery provides:

* Distributed task processing
* Retry system
* Task monitoring
* Concurrency control

---

## Why Redis?

Redis acts as:

* Message broker (queue storage)
* Result backend
* Fast in-memory system
* Lightweight and simple

---

# ⚙️ Concurrency Design

We restrict concurrency to **10 workers**:

```bash
--concurrency=10
```

Why?

Because:

* Each report triggers multiple external API calls
* Prevent hitting rate limits
* Avoid system overload
* Ensure stable performance for 50–100 users

---

# 🛠️ Installation Guide (WSL)

## 1️⃣ Install Redis

```bash
sudo apt update
sudo apt install redis-server
```

Start Redis:

```bash
sudo service redis-server start
```

Check if running:

```bash
redis-cli ping
```

Should return:

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

# 🚀 How To Run The System

---

## 1️⃣ Start Redis

```bash
sudo service redis-server start
sudo service redis-server stop # To stop Redis when done
```

---

## 2️⃣ Start Celery Worker

Instead of typing long command every time:

Run:

```bash
chmod +x queuing/run_worker.sh
./queuing/run_worker.sh
```
or

```bash
bash queuing/run_worker.sh
```

- This does NOT require execute permission.
- So no chmod needed ever.
- This is the simplest fix for your current setup.

This runs:

```bash
celery -A queuing.celery_worker.celery_app worker --loglevel=info --concurrency=10 -E
```

---

## 3️⃣ Start Flask App

```bash
python app.py
```

---

## 4️⃣ Start Flower Monitoring

```bash
chmod +x queuing/run_flower.sh
./queuing/run_flower.sh
```

Open in browser:

```
http://localhost:5555
```

You will see:

* Active tasks
* Failed tasks
* Worker status
* Task duration
* Queue size

---

# 📦 Sending Multiple Tasks (30 at Once)

Run:

```bash
python send_requests.py
```

This automatically sends 30 report generation tasks to Flask.

Celery will:

* Queue them
* Execute max 10 at a time
* Process remaining after completion

---

# 📊 Monitoring Dashboard (Flower)

Flower allows you to monitor:

* Task execution time
* Worker health
* Task failures
* Retries
* Queue backlog

Command:

```bash
celery -A queuing.celery_worker.celery_app flower --port=5555
```

Access:

```
http://localhost:5555
```

---

# 📈 Metrics Logging

Celery logs:

* Task started
* Task completed
* Task failed
* Execution duration

Logs visible in worker terminal.

You can extend this by:

* Logging to file
* Sending metrics to Prometheus
* Integrating Grafana

---

# 🔁 Failure & Retry Strategy

We use:

```python
autoretry_for=(Exception,)
retry_kwargs={'max_retries': 3}
retry_backoff=True
```

### Strategy:

* Retry up to 3 times
* Exponential backoff
* Prevents immediate re-flooding of APIs
* Handles:

  * Network errors
  * LLM API timeout
  * Temporary rate limits

---

# 📈 Scaling Beyond 10 Workers

Current limit: 10 concurrent tasks

If traffic increases:

### Option 1 – Increase Concurrency

```
--concurrency=20
```

Only if:

* System CPU allows
* API rate limits permit

---

### Option 2 – Add Multiple Workers

Run multiple worker processes:

```bash
celery -A queuing.celery_worker.celery_app worker --loglevel=info --concurrency=10 -n worker1@
celery -A queuing.celery_worker.celery_app worker --loglevel=info --concurrency=10 -n worker2@
```

---

### Option 3 – Horizontal Scaling (Production)

* Deploy workers on multiple servers
* Use centralized Redis
* Use load balancer

This is real scaling.

Instead of:

1 machine → 1 worker


You do:

Machine A → 10 workers
Machine B → 10 workers
Machine C → 10 workers


All connected to SAME Redis.

🧠 Why It Works

Redis is centralized broker.

Workers pull tasks independently.

More machines = more throughput.

---

# ⚠️ Edge Cases Handled

| Scenario           | Solution         |
| ------------------ | ---------------- |
| LLM API timeout    | Auto retry       |
| Redis restart      | Worker reconnect |
| Worker crash       | Tasks re-queued  |
| High load spike    | Queue backlog    |
| Duplicate requests | Task ID tracking |

---

# 🔒 Production Improvements (Future)

* Use Redis Cluster
* Use Docker
* Use Supervisor / systemd
* Add rate limiting middleware
* Add authentication for Flask
* Add result persistence (DB)
* Use Kubernetes for scaling

---

# 🧪 Example API Flow

### Generate Report

```
POST /generate
{
  "startup": "TeslaAI"
}
```

Returns:

```
{
  "task_id": "123-xyz"
}
```

---

### Check Status

```
GET /status/<task_id>
```

Returns:

```
{
  "status": "SUCCESS",
  "result": "Generated report..."
}
```

---

# 🧠 Why This Architecture Is Good For VCs

* Handles 50–100 users safely
* Controls expensive LLM usage
* Prevents API overloading
* Scalable design
* Monitored system
* Retry resilient

---

# 🏁 Conclusion

This project demonstrates:

* Distributed task queue design
* Async backend architecture
* Concurrency management
* External API orchestration
* Monitoring & metrics
* Production-ready structure

It is a scalable system suitable for AI-powered research report generation platforms.

---
