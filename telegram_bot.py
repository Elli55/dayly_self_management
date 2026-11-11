import requests as rq
import functions as fc
from dotenv import load_dotenv
import os
from pathlib import Path
import json
import datetime as dt
import DataWork

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

    text = str()
    date = str()
    sender = str()
    data = list()

    try:

        result = rq.get(f'https://api.telegram.org/bot{TOKEN}/getUpdates')

        result.raise_for_status()

        for item in result.json()['result']:

            category = str()

            for i in item['message']['text'].strip().split():
                category = i
                
                break

            print(category, item['message']['text'].strip().split()[-1])
            

            # DataWork.add_telegram_message(item['message']['message_id'],
            #                               item['message']['from']['username'],
            #                               dt.datetime.fromtimestamp(item['message']['date'], tz=dt.timezone.utc).strftime('%Y-%m-%d %H:%M'),
            #                               category,
            #                               item['message']['text'],
            #                               'read'
            #                              )       

    except Exception as e:
        fc.erro_logger(e, 'telegram_bot/get_telegram_result')  

get_telegram_result()
     

def expense_structure(parts):

    expense_name = str()
    expense_category = str()
    expense_amount = str()
    expense_date = str()
    expense_note = str()

        
    if len(parts) == 4:
        expense_name = parts[1]
        expense_category = parts[2]
        expense_amount = parts[3]
        expense_date = parts[4]
        expense_note = 'None'

    elif len(parts) < 4:
        fc.erro_logger('Wrong size Message ', f'Telegram message : {parts}')
        
    elif len(parts) == 5:
        expense_name = parts[1]
        expense_category = parts[2]
        expense_amount = parts[3]
        expense_date = parts[4]
        expense_note = parts[5]
        

    cursor.execute('''INSERT INTO Expenses(name, category, amount, date, note )
                    VALUES(?,?,?,?,?)''', 
                    (expense_name, expense_category, expense_amount, expense_date, expense_note))

    connection.execute()


def income_structure(parts):     

    income_source = str()
    income_amount = str()
    income_date = str()
    income_note = str()


    if len(parts) < 4:

        fc.erro_logger('Wrong message size ', f'Message from telegram : {parts}')

    else:

        income_source = parts[1]
        income_amount = parts[2]
        income_date = parts[3]
        income_note = parts[4]


    cursor.execute('''INSERT INTO Income(source, amount, date, note)
                    VALUES (?, ?, ?, ?)''', (income_source, income_amount, income_date, income_note))

    connection.commit()




def parse_message(text:str):

    parts = text.strip().split()
    
    #Expenses

    

   



