import requests as rq
import functions as fc
from dotenv import load_dotenv
import os
from pathlib import Path
import functions as fc
import datetime as dt
import DataWork
import pandas as pd

BASE = Path(__file__).parent
ENV_FILE = BASE / 'system' / '.env'
load_dotenv(ENV_FILE, encoding='utf-8-sig')

try:
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    if not TOKEN:
        fc.erro_logger('No TOKEN for Telegram', 'first check .env and server')
except Exception as e:
    fc.erro_logger(e, 'telegram_bot/TOKEN')        


connection = fc.connection
cursor = connection.cursor()



def get_telegram_result():

    try:


        result = rq.get(f'https://api.telegram.org/bot{TOKEN}/getUpdates')

        result.raise_for_status()

    except Exception as e:
        fc.erro_logger(e, 'telegram_bot/get_telegram_result/config')

    for item in result.json()['result']:

        try:


            category = str()

            for i in item['message']['text'].strip().split():
                category = i
                
                break 
        
        except Exception as e:
            fc.erro_logger(e, 'telegram_bot/get_telegram_result') 
        

        

        DataWork.add_telegram_message(item['message']['message_id'],
                                        item['message']['from']['username'],
                                        dt.datetime.fromtimestamp(item['message']['date'], tz=dt.timezone.utc).strftime('%Y-%m-%d %H:%M'),
                                        category.lower(),
                                        item['message']['text'],
                                        'read'
                                        )       

    
def parse_message():

    # for creating the DB
    get_telegram_result()


    # expenses
    df_expenses = pd.read_sql('''SELECT * FROM TelegramMessage
     
                                WHERE category ='Expenses'
                                ''')




    

   



