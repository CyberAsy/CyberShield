from datetime import datetime, timedelta

log_file = "logs/login.log"
alert_file = "logs/alerts.log"

failed_attempts = {}

TIME_WINDOW = 60
THRESHOLD = 5

with open(log_file, "r") as file:
    for line in file:
        if "Failed login" not in line:
            continue

        parts = line.split()

        try:
            timestamp = datetime.strptime(
                parts[0] + " " + parts[1],
                "%Y-%m-%d %H:%M:%S"
            )
        except (IndexError, ValueError):
            continue

        ip = None
        username = "unknown"

        if "from" in parts:
            index = parts.index("from")
            if index + 1 < len(parts):
                ip = parts[index + 1]

        for part in parts:
            if part.startswith("username="):
                username = part.replace("username=", "")

        if ip is None:
            continue

        if ip not in failed_attempts:
            failed_attempts[ip] = []

        failed_attempts[ip].append((timestamp, username))

with open(alert_file, "a") as alerts:
    for ip, events in failed_attempts.items():

        events.sort()

        for i in range(len(events)):
            start_time = events[i][0]
            recent_events = [
                event for event in events
                if start_time <= event[0] <= start_time + timedelta(seconds=TIME_WINDOW)
            ]

            if len(recent_events) >= THRESHOLD:
                username = recent_events[-1][1]

                message = (
                    f"Brute-force pattern detected | "
                    f"IP={ip} | "
                    f"Attempts={len(recent_events)} | "
                    f"Username={username} | "
                    f"Window={TIME_WINDOW}s"
                )

                print(f"🚨 {message}")
                alerts.write(message + "\n")
                break
