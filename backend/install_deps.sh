if [ ! -d backend ]; then
    python3 -m venv backend.venv
fi
source ./backend.venv/bin/activate
pip install -r requirements.txt
