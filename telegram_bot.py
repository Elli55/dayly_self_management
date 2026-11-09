import requests as rq
import functions as fc
from dotenv import load_dotenv
import os
from pathlib import Path
import json

BASE = Path(__file__).parent
ENV_FILE = BASE / 'system' / '.env'
load_dotenv(ENV_FILE, encoding='utf-8-sig')

connection = fc.connection
cursor = connection.cursor()

def get_telegram_result():

    try:

        token = os.getenv('TELEGRAM_TOKEN')
        

        result = rq.get(f'https://api.telegram.org/bot{token}/getUpdates')

        result.raise_for_status()

        with open('datas/telegram_logger.jsonl', 'a', encoding='utf-8') as f:
            json.dump(result.json(), f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(e)   

get_telegram_result()         


def parse_message(text:str):

    parts = text.strip().split()
    
    #Income

    expense_name = str()
    expense_category = str()
    expense_amount = str()
    expense_date = str()
    expense_note = str()


    if parts[0].lower() == 'expenses':
        
        if len(parts) == 4:
            expense_name = parts[1]
            expense_category = parts[2]
            expense_amount = parts[3]
            expense_date = parts[4]
            expense_note = 'None'

        if len(parts) < 4:
            fc.erro_logger('Wrong size Message ', f'Telegram message : {text}')
            
        if len(parts) == 5:
            expense_name = parts[1]
            expense_category = parts[2]
            expense_amount = parts[3]
            expense_date = parts[4]
            expense_note = parts[5]
            

        cursor.execute('''INSERT INTO Expenses(name, category, amount, date, note )
                        VALUES(?,?,?,?,?)''', 
                        (expense_name, expense_category, expense_amount, expense_date, expense_note))

        connection.execute()



