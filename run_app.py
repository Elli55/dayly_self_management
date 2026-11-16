import getpass, subprocess, sys, time
from pathlib import Path
import DataWork
import functions as fc
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


if getpass.getpass('\n###########\n\n\nPASSWORD:  ***** ') != correct:
    print('\n #### WRONG KEY ####\n \n#### SHUTTING DOWN #### \n \n if u ar not me dont try, Its good for both of us. Enjoy ur life not my business. ')
    time.sleep(15)
    sys.exit(1)



try: # total connections
    fc.connection
    print('\nConnection is done, just wait configuration \n')
    time.sleep(3)
except Exception as e:
    print('\nSomething wrong with connection\n')
    fc.erro_logger(e,'runn_app/connections')

try: # balance update
    DataWork.update_balance()
    print('DB workwell\n')
    time.sleep(3)
except Exception as e :
    print('Something wrong  with DB \n')
    fc.erro_logger(e, 'run_app/balance_update')


server = subprocess.Popen(
    [sys.executable, '-m', 'streamlit', 'run', 'finance_app.py',
     '--server.headless', 'true',
     '--server.port', '8501',
     '--server.address', 'localhost'],
    cwd=BASE,
)

print('Getting start few seconds.......------ \n')
time.sleep(5)
if browser:
    subprocess.Popen([browser, f'--app={URL}'])
else:
    print(f'no BROWSER_PATH found. Manual open : {URL}')


try:
    server.wait()
except KeyboardInterrupt:
    server.terminate()