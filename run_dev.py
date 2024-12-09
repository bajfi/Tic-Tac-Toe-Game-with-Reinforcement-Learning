import subprocess
import time
import webbrowser


def main():
    # Start Flask server
    print("Starting Flask server...")
    flask_process = subprocess.Popen(
        ["python", "backend/app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Wait for server to start
    time.sleep(2)

    # Open browser
    print("Opening browser...")
    webbrowser.open("http://localhost:5000")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        flask_process.terminate()


if __name__ == "__main__":
    main()
