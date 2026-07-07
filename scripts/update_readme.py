import re
import subprocess
from datetime import datetime, timezone, timedelta


def get_commit_streak() -> int:
    log = subprocess.check_output(
        ["git", "log", "--format=%ad", "--date=short"],
        text=True
    ).strip().splitlines()

    if not log:
        return 0

    dates = sorted(set(log), reverse=True)
    today = datetime.now(timezone.utc).date()
    streak = 0

    for i, date_str in enumerate(dates):
        day = datetime.strptime(date_str, "%Y-%m-%d").date()
        expected = today - timedelta(days=i)
        if day == expected:
            streak += 1
        else:
            break

    return streak


def get_total_commits() -> int:
    result = subprocess.check_output(
        ["git", "rev-list", "--count", "HEAD"],
        text=True
    ).strip()
    return int(result)


def days_since_start() -> int:
    # Change this to the date you started your GitHub journey
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - start).days


def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    streak        = get_commit_streak()
    total_commits = get_total_commits()
    active_days   = days_since_start()
    last_updated  = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    replacements = {
        r"STREAK:\s+\d+":        f"STREAK:        {streak}",
        r"TOTAL_COMMITS:\s+\d+": f"TOTAL_COMMITS: {total_commits}",
        r"ACTIVE_DAYS:\s+\d+":   f"ACTIVE_DAYS:   {active_days}",
        r"LAST_UPDATED:\s+.+":   f"LAST_UPDATED:  {last_updated}",
    }

    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"streak={streak} | commits={total_commits} | days={active_days}")


if __name__ == "__main__":
    update_readme()
