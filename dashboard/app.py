from flask import Flask, render_template
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGIN_LOG = os.path.join(BASE_DIR, "logs", "login.log")
ALERT_LOG = os.path.join(BASE_DIR, "logs", "alerts.log")


def read_log(path):
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def count_results(events):
    successful = sum("Successful login" in event for event in events)
    failed = sum("Failed login" in event for event in events)

    return successful, failed


@app.route("/")
def dashboard():
    login_events = read_log(LOGIN_LOG)
    alert_events = read_log(ALERT_LOG)

    successful_logins, failed_logins = count_results(login_events)

    return render_template(
        "dashboard.html",
        login_count=len(login_events),
        successful_count=successful_logins,
        failed_count=failed_logins,
        alert_count=len(alert_events),
        recent_events=login_events[-5:],
        recent_alerts=alert_events[-5:]
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5050,
        debug=True
    )
