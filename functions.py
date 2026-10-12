# for functions, API connection and AI

import pandas as pd
import sqlite3 as sq
import json
import datetime
from pathlib import Path
import streamlit as st


# logging

def erro_logger(e, location):

    data = {
        'time': datetime.datetime.now().strftime('%Y.%m.%d.%H:%M:%S'),
        'type_of_error':type(e).__name__,
        'error': str(e),
        'location':  location
    }

    with open('system/error_logging.jsonl', 'a', encoding='utf-8') as f:
        json.dump(data, f,  ensure_ascii=False, indent=4 )

def proces_logger(mesagge : str, location : str):

    data = {
        'time': datetime.datetime.now().strftime('%Y.%m.%d.%H:%M:%S'),
        'Location': location,
        'Message': mesagge

    }

    with open('system/proces_logging.jsonl', 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



# connections


@st.cache_resource
def get_connection():
    return sq.connect('datas/finance.db', check_same_thread=False)

connection = get_connection()




Path('datas').mkdir(exist_ok=True)
Path('system').mkdir(exist_ok=True)



# globals

DATE_OF_DAY = datetime.datetime.today().strftime('%Y-%m-%d')
TODAY = datetime.date.today()
WEEK_TODAY = datetime.date.today().weekday()
MONDAY = TODAY - datetime.timedelta(days=WEEK_TODAY)





PAGE_NAMES = ['Dayly Dashboard', 'Finance', 'Data Entery', 'Math']

CATEGORY_FOR_EXPENSES = ['Food', 'Food Out Side','Alchohol', 'Cigarette',
                         'Rent','Clothes','Education','Gift','Debitor','Invest',
                         'Cleaning', 'Maintenace Staff','Travel', 'Family']

CATEGORY_LIMITS_FOR_EXPENSES = {'Food': {'low': 50, 'limit':150},
                        'Alchohol': {'low': 25, 'limit':60},
                        'Cigarette':{'low':10, 'limit':30},
                        'Education': {'low': 300, 'limit':1000},
                        'Debitor': {'low': 150, 'limit':200},
                        'Cleaning': {'low': 10, 'limit':50},
                        'Maintenace Staff': {'low': 20, 'limit':50},
                        'Family':{'low': 150, 'limit':300},
                        'Travel':{'low':20, 'limit':100},
                        'Kreditor':{'low':150, 'limit':500},
                        'Gift':{'low':20, 'limit':100},
                        'Rent':{'low':250, 'limit':500},
                        'Invest':{'low':100, 'limit':500},
                        'Food Out Side':{'low':50, 'limit':100},
                        'Clothes':{'low':10, 'limit':50}}


INCOME_SOURCE = ['Tips', 'Work', 'Schollership',  'Kreditor', 'Invest']

try:

    LIST_OF_DATES_FOR_EXPENSES = pd.read_sql('''SELECT strftime('%Y-%m', date) as month FROM Expenses ''', connection)['month'].unique().tolist()
except Exception as e:
    LIST_OF_DATES_FOR_EXPENSES = []
    erro_logger(e, 'function/list_of_dates_for_expenses') 

WORKED_COMPANIES = {'BrinkGeherMeyer':{'montly_hours':80, 'salary':980}, 
                    'Rampendahl ':{'montly_hours':0, 'salary':0}} 

DONOR_SCHOLLERSHIPS = ['BaFög', 'IPS']

PLANNER_CATEGORIES = ['Work', 'Study','Sport','Tanze', 'Task', 'Personal', 'Fun']

PLANNER_COLOURS = { 
    'Work':     "#d84c10",
    'Study':    "#0f3808",
    'Task':     '#f0a500',
    'Sport':    "#362D0A",
    'Personal': '#b57f00', 
    'Fun':      "#551068",
    'Tanze':    "#0B42D8"
    }


HABITS = ['Sport', 'Reading', 'Math']









# css 
def load_css():
    with open('style.css') as f:
        return f'<style> {f.read()} </style>'



## 1 page   



def generate_metric_card(title: str, value, delta, last, delta_sign='%',
                         higher_is_better=True, last_label='Last month'):

    if delta is None or delta == 0:
        arrow, tone, delta_text = '–', 'neutral', '–'
    else:
        arrow = '▲' if delta > 0 else '▼'
        tone = 'positive' if (delta > 0) == higher_is_better else 'negative'
        delta_text = f'{abs(delta)} {delta_sign}'

    return f'''<section class='metric_card background_{tone}'>
        <p class='title_of_matric_card'> {title} </p>
        <h2 class='value_of_metric_card font_{tone}'> {value} </h2>
        <p class='delta_of_metric_card'> {arrow} {delta_text} </p>
        <p class='last_of_metric_card'> {last_label}: {last:,.2f} € </p>
        </section>'''






def generate_total_cards(amount: float = 0.0 , ineverse: bool = True):

    try: 
        if ineverse == True:
            background_colour = 'background_positive' if amount > 0 else 'background_negative'
            font_colour = 'font_positive' if amount > 0 else 'font_negative'
        else:
            background_colour = 'background_positive' if amount < 0 else 'background_negative'
            font_colour = 'font_positive' if amount < 0 else 'font_negative'

        return f'''<section class='{background_colour}'>
                <p class='element_total_card {font_colour}'>{amount}</p>
                </section>'''
    
    except Exception as e:
        erro_logger(e, 'functions/generate_total_cards')

            



## 2 page 

def generate_delta(last, current):

    if not current:
        return None
    else:
        return round((current- last) / abs(last) * 100, 2)



def get_category_colour(category, amount):

    limit = CATEGORY_LIMITS_FOR_EXPENSES.get(category, {'low': 200, 'limit': 500})


    if amount < limit['low']:

        colour =  "#19C406" 

    elif amount < limit['limit']:

        colour =  "#FBFF00"  

    else:
        colour = '#ff0000'    

    return colour    









 

