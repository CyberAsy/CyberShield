from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "logs/login.log"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        ip = request.remote_addr
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # بيانات تجريبية فقط للمختبر
        if username == "admin" and password == "CyberShield123":
            status = "Successful login"
        else:
            status = "Failed login"

        with open(LOG_FILE, "a") as log:
            log.write(
                f"{timestamp} {status} from {ip} username={username}\n"
            )

        return render_template("login.html", message=status)

    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
