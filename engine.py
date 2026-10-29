import os
import sys
import time
import subprocess
import requests

TARGET_FILE = os.path.join(os.path.dirname(__file__), "sandbox", "app.py")
MAX_GENERATIONS = 5
PORT = 5000
URL = f"http://127.0.0.1:{PORT}/add"

# Defensive code that the AI Coder agent outputs
FIXED_APP_CODE = """from flask import Flask, request

app = Flask(__name__)
data_store = []

@app.route('/add', methods=['POST'])
def add_data():
    data = request.json or {}
    # Evolved Code: Safe key check prevents server crash
    item = data.get('item', 'default_item')
    data_store.append(item)
    return "Data added successfully!", 200

if __name__ == '__main__':
    app.run(port=5000)
"""


def mock_swarm_fix():
    print("[Agent Swarm - Detective]: Identified KeyError 'item' in sandbox/app.py.")
    time.sleep(1)
    print("[Agent Swarm - Architect]: Formulated patch plan using dict.get() fallback.")
    time.sleep(1)
    print(
        "[Agent Swarm - Coder]: Writing defensive error-handling patch to sandbox/app.py..."
    )
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(FIXED_APP_CODE)
    print("[Agent Swarm]: Patch successfully applied to sandbox/app.py.")


def run_simulation():
    generation = 1
    while generation <= MAX_GENERATIONS:
        print("\n==========================================")
        print(f"       GENERATION {generation} of {MAX_GENERATIONS}")
        print("==========================================")

        python_bin = sys.executable
        print("[System] Booting sandbox target app...")
        process = subprocess.Popen([python_bin, TARGET_FILE])
        time.sleep(2)

        print("[System] Firing extinction stressor payload...")
        crash_log = None
        try:
            response = requests.post(URL, json={"wrong_key": "data"}, timeout=3)
            if response.status_code >= 500:
                crash_log = f"HTTP {response.status_code} Internal Server Error"
        except Exception as e:
            crash_log = f"Connection error: {str(e)}"

        process.terminate()
        process.wait()
        time.sleep(1)

        if not crash_log:
            print("\n[SUCCESS] Sandbox app survived the stressor!")
            print(f"Check sandbox/app.py to view updated code.")
            break

        print(f"\n[CRASH DETECTED] {crash_log}")
        print("[System] Triggering AI Swarm to rewrite code...\n")
        mock_swarm_fix()

        generation += 1


if __name__ == "__main__":
    run_simulation()
