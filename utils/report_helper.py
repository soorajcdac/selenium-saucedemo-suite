import os
import json
from datetime import datetime


def save_run_summary(passed, failed, duration):
    """
    Save a JSON summary of the test run to reports/.
    Useful for tracking history across multiple runs.
    """
    os.makedirs("reports", exist_ok=True)
    summary = {
        "timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "passed":     passed,
        "failed":     failed,
        "total":      passed + failed,
        "duration_s": round(duration, 2),
        "status":     "PASS" if failed == 0 else "FAIL"
    }
    path = f"reports/run_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\n📋 Run summary saved: {path}")
    return path


def get_screenshot_list():
    """Return list of all screenshots in reports/screenshots/."""
    folder = "reports/screenshots"
    if not os.path.exists(folder):
        return []
    return [
        f for f in os.listdir(folder)
        if f.endswith(".png")
    ]


def print_run_banner(base_url, browser, workers=1):
    """Print a formatted banner at the start of a test run."""
    print("\n" + "=" * 60)
    print("  🧪  SELENIUM AUTOMATED TEST SUITE")
    print("=" * 60)
    print(f"  🌐  URL      : {base_url}")
    print(f"  🖥️   Browser  : {browser}")
    print(f"  ⚡  Workers  : {workers}")
    print(f"  🕐  Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")