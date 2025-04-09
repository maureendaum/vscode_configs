# Python VSCode `launch.json` sample project

This small repository is intended to show sample `launch.json` configurations for common python debugging scenarios.
The web server and celery process are only intended to be targets for debugging, not to provide useful functionality.

It includes configurations to:
* Start a FastAPI web server
* Start a Celery instance with Redis as a broker. The configuration also launches Redis and shuts it down.
* Run tests using `pytest`

## Set up
This project assumes you have `docker` available.

To set up the python environment, create a virtual environment and install the requirements.
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

After you open the project in VSCode, set the virtual environment as the interpreter.
Note that this assumes you have the Python and Python Debugger extensions installed.
```
cmd + shift + P > Python: Select Interpreter > ./.venv/bin/python
```

## Usage
The following video shows the workflow of launching debug processes, setting breakpoints, and using the debug console (`cmd + shift + y`) to inspect variables.
