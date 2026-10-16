import getpass, subprocess, sys, time
from pathlib import Path
import os
from dotenv import load_dotenv

BASE = Path(__file__).parent
ENV_FILE = BASE / 'system' / '.env'
load_dotenv(ENV_FILE, encoding='utf-8-sig')


URL = 'http://localhost:8501'



correct = os.getenv('APP_PASSWORD')
browser = os.getenv('BROWSER_PATH')

if not correct:
    print('Passwort ist empty or problem with .env')
    input('Tab any button')
    sys.exit(1)


if getpass.getpass('Passwort: ') != correct:
    print('Wrong key')
    time.sleep(2)
    sys.exit(1)


server = subprocess.Popen(
    [sys.executable, '-m', 'streamlit', 'run', 'finance_app.py',
     '--server.headless', 'true',
     '--server.port', '8501',
     '--server.address', 'localhost'],
    cwd=BASE,
)


time.sleep(5)
if browser:
    subprocess.Popen([browser, f'--app={URL}'])
else:
    print(f'no BROWSER_PATH found. Manual open : {URL}')


try:
    server.wait()
except KeyboardInterrupt:
    server.terminate()