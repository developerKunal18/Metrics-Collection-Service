from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

metrics = {
    "total_requests": 0,
    "total_errors": 0,
    "average_response_time": 0
}

response_times = []


# ---------- Middleware ----------
@app.before_request
def before_request():

    request.start_time = datetime.now()


@app.after_request
def after_request(response):

    metrics["total_requests"] += 1

    elapsed = (
        datetime.now()
        - request.start_time
    ).total_seconds()

    response_times.append(elapsed)

    metrics[
        "average_response_time"
    ] = (
        sum(response_times)
        /
        len(response_times)
    )

    if response.status_code >= 400:

        metrics["total_errors"] += 1

    return response


# ---------- APIs ----------
@app.route("/")
def home():

    return jsonify({
        "message":
        "Metrics Service Running"
    })


@app.route("/error")
def error():

    return jsonify({
        "message":
        "Error"
    }), 500


@app.route("/metrics")
def get_metrics():

    return jsonify(metrics)


@app.route("/health")
def health():

    return jsonify({
        "status":
        "healthy"
    })


if __name__ == "__main__":

    app.run(
        debug=True
    )
