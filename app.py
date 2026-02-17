from flask import Flask, jsonify, request
from tasks import generate_report
from celery_worker import celery

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    startup_name = data.get("startup")

    task = generate_report.delay(startup_name)

    return jsonify({
        "job_id": task.id,
        "status": "queued"
    })


@app.route('/status/<job_id>', methods=['GET'])
def check_status(job_id):
    task = celery.AsyncResult(job_id)

    response = {
        "job_id": job_id,
        "state": task.state,
        "result": task.result if task.state == "SUCCESS" else None
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
