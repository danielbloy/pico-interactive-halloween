# From: https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/
cd /home/daniel/pico-interactive-halloween
source audio_venv/bin/activate
export PYTHONPATH=/home/daniel/pico-interactive
cd desktop/background
python3 main.py
