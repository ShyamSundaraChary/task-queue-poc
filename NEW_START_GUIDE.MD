
---

# ✅ Your Gunicorn Script Explained (RabbitMQ Version)

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

# 🧠 Important Concept (Updated Architecture)

Gunicorn handles:

👉 **HTTP requests**

Celery handles:

👉 **Background tasks**

RabbitMQ handles:

👉 **Queue storage (broker)**

Redis handles:

👉 **Task results storage**

They are separate processes.

---

# 🏗️ Final Production Flow (With RabbitMQ)

```
Client
   ↓
Gunicorn (2 workers)
   ↓
Flask App
   ↓
Celery
   ↓
RabbitMQ (Message Broker)
   ↓
Celery Worker (concurrency = 4 or 10)
   ↓
LLM APIs
   ↓
Redis (Result Backend)
   ↓
Client polls status
```

---

# 🚀 How To Run Everything Now (RabbitMQ Version)

Open **5 terminals** in WSL.

---

## 🖥️ Terminal 1 — Start RabbitMQ

```bash
sudo service rabbitmq-server start
```

Verify:

```bash
sudo rabbitmqctl status
```

Open UI:

```
http://localhost:15672
```

Login:

```
guest / guest
```

---

## 🖥️ Terminal 2 — Start Redis (Result Backend)

```bash
sudo service redis-server start
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

## 🖥️ Terminal 3 — Start Celery Worker

Make sure your `celery_worker.py` has:

```python
BROKER_URL = "amqp://guest:guest@localhost:5672//"
BACKEND_URL = "redis://localhost:6379/1"
```

Now run:

```bash
source venv/bin/activate
bash queuing/run_worker.sh
```

You should see:

```
Connected to amqp://guest@localhost:5672//
Ready.
```

---

## 🖥️ Terminal 4 — Start Gunicorn

Make script executable (only first time):

```bash
chmod +x run_api.sh
```

Run:

```bash
source venv/bin/activate
./run_api.sh
```

Server now running on:

```
http://localhost:8000
```

---

## 🖥️ Terminal 5 — Start Flower

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

# 🔍 What You Will See (Now With RabbitMQ)

## 🐰 In RabbitMQ UI (Queue-Level Monitoring)

Go to:

```
Queues → celery
```

You will see:

| Field     | Meaning                     |
| --------- | --------------------------- |
| Ready     | Waiting tasks (not started) |
| Unacked   | Currently running tasks     |
| Total     | Total tasks in system       |
| Consumers | Number of active workers    |

This is what Redis could not clearly show.

---

## 🌸 In Flower (Task-Level Monitoring)

You will see:

* Active tasks
* STARTED
* SUCCESS
* FAILURE
* Worker concurrency

---

# 🔥 How To See Queue Size Now

Instead of Redis CLI:

Open RabbitMQ UI → Queues → celery

You’ll see something like:

```
Ready: 20
Unacked: 10
Total: 30
```

Meaning:

* 10 running
* 20 waiting
* 0 completed

Exactly what you wanted.

---

# ⚙️ Recommended Production Improvements (RabbitMQ Setup)

## 1️⃣ Durable Queue + Persistent Messages

Inside `celery_worker.py` add:

```python
celery_app.conf.task_default_delivery_mode = "persistent"
```

This ensures tasks survive broker restart.

---

## 2️⃣ Recommended Worker Settings (2 CPU / 4GB)

For your AWS-like machine:

```
--concurrency=4
--prefetch-multiplier=1
--max-tasks-per-child=20
```

Safe and stable.

---

## 3️⃣ Gunicorn Worker Rule

Check CPU:

```bash
nproc
```

Rule:

```
workers = (2 × CPU cores) + 1
```

But since tasks are async (Celery handles heavy work):

2 workers is usually enough.

---

# 📊 Monitoring Summary (Updated)

| Component     | How To Monitor  |
| ------------- | --------------- |
| Gunicorn      | Terminal logs   |
| Celery Worker | Worker terminal |
| Queue Size    | RabbitMQ UI     |
| Running Tasks | Flower          |
| Completed     | Flower          |
| Results       | Redis backend   |

---

# 🏁 Final Confirmation Checklist

If:

* RabbitMQ running
* Redis running
* Worker connected to amqp
* Gunicorn running
* Flower running
* You send 30 requests
* RabbitMQ shows Ready + Unacked
* Tasks process gradually

Then your system is now:

- ✅ Proper message broker architecture
- ✅ Production-grade queue visibility
- ✅ Horizontally scalable
- ✅ Architecturally clean
- ✅ LLM-safe backend

---

Shyam — this is now a **real distributed system architecture**.

If you want next, I can help you:

* Add Dead Letter Queue (for failed LLM calls)
* Secure RabbitMQ (non-guest user)
* Deploy this cleanly on AWS EC2
* Dockerize the full stack properly

Tell me your next move 👌
