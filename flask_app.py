from flask import Flask, request, jsonify
from concurrent.futures import ProcessPoolExecutor
import subprocess
import json
import os
import logging
import secrets
from threading import Lock
from time import sleep
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["2 per second"]
)

# Configure process pool
process_pool = ProcessPoolExecutor(max_workers=4)

# Thread-safe counter for tracking active processes
active_processes_lock = Lock()
active_processes = 0


import psutil

def check_system_resources():
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    return cpu_percent < 80 and memory_percent < 80

class TrendsScrapping:
    def __init__(self):
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def run_ts_script(self, query):
        """
        Run the selenium script and return its output data

        Args:
            query (str): Search query for trends

        Returns:
            dict: Scraped trends data
        """
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            script_path = os.path.join(current_dir, 'trends-api.ts')

            # Start the script as a subprocess
            process = subprocess.Popen(
                ['bun', script_path, query],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            self.logger.info(f"Started ads_power_selenium.py script with query: {query}")

            # Poll process for new output until finished
            stdout = []
            stderr = []
            while True:
                stdout_line = process.stdout.readline() if process.stdout else ''
                stderr_line = process.stderr.readline() if process.stderr else ''

                if stdout_line:
                    stdout.append(stdout_line)
                    self.logger.info(f"Script output: {stdout_line.strip()}")
                if stderr_line:
                    stderr.append(stderr_line)
                    self.logger.error(f"Script error: {stderr_line.strip()}")

                if process.poll() is not None:
                    break

                sleep(0.1)

            # Get remaining lines after process finishes
            stdout.extend(process.stdout.readlines() if process.stdout else [])
            stderr.extend(process.stderr.readlines() if process.stderr else [])

            if process.returncode != 0:
                error_msg = ''.join(stderr)
                self.logger.error(f"Script failed with return code {process.returncode}: {error_msg}")
                raise Exception(f"Selenium script failed: {error_msg}")

            # Parse the JSON output from the script
            try:
                output = ''.join(stdout)
                return json.loads(output)
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse script output as JSON: {output}")
                raise Exception(f"Failed to parse script output: {str(e)}")

        except Exception as e:
            self.logger.error(f"Error running selenium script: {str(e)}")
            raise
        finally:
            # Decrease active process counter
            global active_processes
            with active_processes_lock:
                active_processes -= 1

trends_scrapper = TrendsScrapping()


@app.route('/get_trends_data')
@limiter.limit("2 per second")
def get_trends_data():
    """
    Endpoint to execute selenium script and return trends data
    """
    global active_processes

    # if not check_system_resources():
    #     return jsonify({
    #         'status': 'error',
    #         'message': 'System resources are currently overloaded'
    #     }), 503

    try:
        # Check if we can accept more processes
        with active_processes_lock:
            if active_processes >= 10:  # Maximum concurrent processes
                return jsonify({
                    'status': 'error',
                    'message': 'Server is at maximum capacity. Please try again later.'
                }), 503
            active_processes += 1

        # Get query parameter
        query = request.args.get('query')
        if not query:
            with active_processes_lock:
                active_processes -= 1
            return jsonify({
                "status": "error",
                "message": "Query parameter is required"
            }), 400

        # Submit the task to the process pool
        future = process_pool.submit(trends_scrapper.run_ts_script, query)

        # Get the result with a timeout
        data = future.result(timeout=300)  # 5 minute timeout

        return jsonify({
            "status": "success",
            "data": data
        }), 200

    except TimeoutError:
        return jsonify({
            "status": "error",
            "message": "Operation timed out"
        }), 504
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# Graceful shutdown handler
def cleanup():
    process_pool.shutdown(wait=True)


# Register cleanup handler
import atexit

atexit.register(cleanup)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
