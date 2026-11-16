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
                                        category,
                                        item['message']['text'],
                                        'read'
                                        )       

    
def parse_message():

    # for creating the DB
    get_telegram_result()


    # expenses
    try:

        for _, line in pd.read_sql("SELECT * FROM TelegramMessage WHERE category ='Expenses'",
                                   connection).iterrows():

            text_elements = line['text'].strip().split()

            if len(text_elements) <= 3 or len(text_elements) > 5:

                DataWork.change_status_of_tg_message(line['id'], 'error')

            elif len(text_elements) == 5:
                DataWork.write_expenses(text_elements[1],
                                        text_elements[2],
                                        text_elements[3],
                                        line['date'][:10],
                                        text_elements[4])

                DataWork.change_debit_status(line['id'], 'done')

            elif len(text_elements) == 4:

                DataWork.write_expenses(text_elements[1],
                                        text_elements[2],
                                        text_elements[3],
                                        line['date'][:10],
                                        'None')

                DataWork.change_debit_status(line['id'], 'done')
            else:
                fc.erro_logger(f'Error in calculation: {text_elements}', 'telegram_bot/parse_message/expenses')
                continue
            
    except Exception as e:
        fc.erro_logger(e, 'telegram_bot/parse_message/expenses')


    # worked hours 

    try:    

        for _, line in pd.read_sql("SELECT * FROM TelegramMessage WHERE category = 'Worked'",
                                connection).iterrows():

            text_elements = line['text'].strip().split()

            if len(text_elements) < 4 or len(text_elements) < 4:
                DataWork.change_status_of_tg_message(line['id'], 'error')

            elif len(text_elements) == 4:

                DataWork.write_work_hours(text_elements[1],
                                        line['date'][:10],
                                        text_elements[2],
                                        text_elements[3],
                                        fc.WORKED_COMPANIES[text_elements[1]].get('per_hour'))

            else:

                fc.erro_logger(f'Error in calculation: {text_elements}', 'telegram_bot/parse_message/expenses')
                continue
            
    except Exception as e:
        fc.erro_logger(e, 'telegram_bot/parse_message/worked_hours')




                

            



