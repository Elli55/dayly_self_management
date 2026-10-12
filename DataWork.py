import sqlite3 as sq
import functions
import pandas as pd
from datetime import datetime


connection = functions.get_connection()
corsor = connection.cursor()




# planner

def add_plan_element(title, category, date, start_time, end_time, note):

    try:


        corsor.execute('''

                CREATE TABLE IF NOT EXISTS Planner (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                category TEXT,
                date TEXT,
                start TEXT,
                end TEXT,
                note TEXT
                )

            ''')

        corsor.execute('''

                INSERT INTO Planner (title, category, date, start, end, note)
                VALUES (?,?,?,?,?,?)

            ''', (title, category, str(date), str(start_time), str(end_time), note)) 

        
        connection.commit()

    except Exception as e:
        functions.erro_logger(e, 'DataWorks/add_plan_element')


def delete_from_planner(plan_id):

    try:

        corsor.execute('''

            DELETE FROM Planner WHERE id=?

            ''', (plan_id,))
        connection.commit()
        
    except Exception as e:
        functions.erro_logger(e, 'DataWorks/delete_from_planner')



def df_planner():

    try:

        df_planner = pd.read_sql(''' SELECT * FROM Planner ''', connection)
    except Exception as e:
        functions.erro_logger(e, 'DataWorks/df__planner')    
        df_planner = pd.DataFrame()

    return df_planner    


# habits

def add_habbit(habit, day):

    try:
        corsor.execute('''

            CREATE TABLE IF NOT EXISTS Habits(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            done INTEGER DEFAULT 0
            )

            ''')
        
        corsor.execute('''

            INSERT INTO Habits (name, date)
            VALUES (?,?)

            ''', (habit, day))

        connection.commit()

    except Exception as e:
        functions.erro_logger(e, 'DataWorks/add_habit')


def create_habits_table():

    try:
        corsor.execute('''

            CREATE TABLE IF NOT EXISTS Habits(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            done INTEGER DEFAULT 0
            )

            ''')
        connection.commit()

    except Exception as e:
        functions.erro_logger(e, 'DataWork/create_habits_table')



def toggle_habit(habit, day):

    try:
        corsor.execute('''
        
                    CREATE TABLE IF NOT EXISTS Habits(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    date TEXT,
                    done INTEGER DEFAULT 0
                    )
        
                    ''')

        line = corsor.execute('''SELECT id, done FROM Habits
                                WHERE name = ? AND date = ?''', (habit, str(day))).fetchone()

        if line is None:
            corsor.execute('''INSERT INTO Habits (name, date, done)
                              VALUES (?,?,1)''', (habit, str(day)))
        else:
            new_value = 0 if line[1] == 1 else 1
            corsor.execute('UPDATE Habits SET done = ? WHERE id = ?', (new_value, line[0]))

        connection.commit()

    except Exception as e:
        functions.erro_logger(e, 'DataWork/toggle_habit')


def get_done_days():

    try:

        corsor.execute('''

                CREATE TABLE IF NOT EXISTS Habits(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                date TEXT,
                done INTEGER DEFAULT 0
                )

                ''')

        lines = corsor.execute('''

                SELECT name, date FROM Habits
                WHERE done = 1

                ''').fetchall()

        done_list = dict()

        for name, day in lines:
            if name not in done_list:
                done_list[name] = set()
            done_list[name].add(day)

        return done_list    

    except Exception as e:

        functions.erro_logger(e, 'DataWorks/get_done_days')        


# Todos

def add_todos(todo, category, time_request):

    try:

        corsor.execute('''

                CREATE TABEL IF NOT EXISTS (
                
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                category TEXT,
                time_request REAL,
                done INTEGER DEFAULT 0,
                created_date TEXT,
                done_date TEXT DEFAULT None
                
                )

                ''')

        corsor.execute('''

                INSERT INTO Todos(title, category, time_request, created_date)
                VALUES(?,?,?)

                ''', (todo, category, time_request,functions.DATE_OF_DAY,))

        connection.commit()
    
    except Exception as e:
        functions.erro_logger(e, 'DataWork/add_todos')


def delete_todo(todo_id):

    try:
        corsor.execute('''

                DELETE FROM Todos
                WHERE id = ?

            ''', (todo_id))

        connection.commit()

    except Exception as e:
        functions.erro_logger(e, 'DataWork/delete_todo')



def well_done_todo(todo_id):

    try:

        corsor.execute('''
        
                UPDATE Todos
                SET done = 1 AND done_date = ?
                WHERE id = ?

        ''', (functions.DATE_OF_DAY, todo_id))

        connection.commit()

    except Exception as e:
        functions.erro_logger(e, 'DataWork/well_done_todo')


def df_todos():

    try:

        return pd.read_sql('''

            SELECT * FROM Todos
            WHERE done = 0

                ''')

    except Exception as e:
        functions.erro_logger(e, 'DataWork/df_todos') 
        return pd.DataFrame()   



    


# Not down briefly

def add_briefly_note(note ):
    try:

        corsor.execute('''

            CREATE TABLE Notes IF NOT EXISTS (
            
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note TEXT,
            pinned INTEGER DEFAULT 0,
            added_date TEXT
            )

            ''')

        corsor.execute('''

            INSERT INTO Notes (note, added_date)
            VALUES(?,?)

            ''', (note, functions.DATE_OF_DAY))

    except Exception as e:
        functions.erro_logger(e, 'DataWork/add_briefly_note')  

def delete_note(note_id):

    print('')          




# balance

def update_balance():

    try:
        sum_of_expenses = pd.read_sql('SELECT SUM(amount) FROM Expenses', connection).iloc[0, 0]
        sum_of_income = pd.read_sql('SELECT SUM(amount) FROM Income', connection).iloc[0,0]
        balance =  sum_of_income - sum_of_expenses

        corsor.execute('''

                    CREATE TABLE IF NOT EXISTS Balance(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date  TEXT,
                    balance REAL 
                    )

                    ''')

        corsor.execute('''INSERT INTO Balance(date, balance)
                            VALUES(?,?)

                                ''', (functions.DATE_OF_DAY, balance))

        connection.commit()

        functions.proces_logger(f'for {functions.DATE_OF_DAY} balance refreshed currrent Balance : {balance}', 'DataWork/update_balance')

    except Exception as e:

        functions.erro_logger(e, 'DataWork/update_balance')


        

# expenses

def write_expenses(expense, amount, category, date,note):

    try:
        corsor.execute('''
                CREATE TABLE IF NOT EXISTS Expenses(
                
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    amount REAL,
                    category TEXT,
                    date TEXT,
                    note TEXT)
                    ''')

        corsor.execute(f'''

                INSERT INTO Expenses(name, amount,category,  date, note) VALUES(?,?,?,?,?)''',
                  (expense,amount,category, date, note))
        
        connection.commit()

        functions.proces_logger(f'{amount} - {expense} for {functions.DATE_OF_DAY} added to Expenses Table ', 'DataWork/write_expenses' )
    except Exception as e:
        functions.erro_logger(e, 'DataWork/write_expenses')



def delete_expenses(name, date):

    try:
        corsor.execute('''
                DELETE FROM Expenses WHERE name = ? AND date = ?  

                    ''', (name, date))

        connection.commit()

        functions.proces_logger(f'Deleted from Expenses {name} in {date}')

    except Exception as e:
        functions.erro_logger(e, 'DataWork/delete_expenses')                


# income 

def write_income(source,  amount,date, note):

    try:
        corsor.execute('''
            CREATE TABLE IF NOT EXISTS Income(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            amount REAL,
            date TEXT,
            note TEXT)
            ''')

        corsor.execute(f'''

            INSERT INTO Income(source,  amount, date,note) VALUES (?,?,?,?)''',
              (source,amount,date,note)

            )

        connection.commit()

        functions.proces_logger(f'{amount} EUR from {source} added to Income Table', 'DataWork/write_income')
    except Exception as e:

        functions.erro_logger(e, 'DataWork/write_income')   


def delete_income(name, date):

    try:
        corsor.execute('''

                DELETE FROM Income WHERE source = ? AND date = ?

                ''', (name, date))

        connection.commit()

        functions.proces_logger(f'{name} - {date} from Income deleted ')

    except Exception as e:
        functions.erro_logger(e, 'DataWorks/delete_income')



# works 

def write_work_hours(company, date_of_work, start_time, end_time, salary_per_hour):
    try:
        
        fmt = '%H:%M:%S'
        start = datetime.strptime(str(start_time), fmt)
        end   = datetime.strptime(str(end_time),   fmt)
        total_hours = round((end - start).total_seconds() / 3600, 2)

        if total_hours <= 0:
            functions.erro_logger('End time must be after start time', 'DataWork/write_work_hours')
            return

        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS WorkHours(
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                company         TEXT,
                date_of_work    TEXT,
                start_time      TEXT,
                end_time        TEXT,
                total_hours     REAL,
                salary_per_hour REAL,
                montly_hours    REAL,
                payed           INTEGER DEFAULT 0,
                date_of_day     TEXT)
        ''')
        cursor.execute(
            '''INSERT INTO WorkHours
               (company, date_of_work, start_time, end_time, total_hours, salary_per_hour, montly_hours, payed, date_of_day)
               VALUES(?,?,?,?,?,?,?,0,?)''',
            (company, str(date_of_work), str(start_time), str(end_time),
            total_hours, salary_per_hour, 
            functions.WORKED_COMPANIES.get(f'{company}').get('montly_hours'), 
            functions.DATE_OF_DAY)
        )

        connection.commit()

        functions.proces_logger(
            f'{company} | {date_of_work} | {start_time}-{end_time} | {total_hours}h added',
            'DataWork/write_work_hours'
        )

    except Exception as e:
        functions.erro_logger(e, 'DataWork/write_work_hours')


def payed_from_works(work_place, date_of_pay,start_date, end_date):
    try:
        cursor = connection.cursor()
        
        df = pd.read_sql(
            '''SELECT * FROM WorkHours
               WHERE company = ? AND DATE(date_of_work) BETWEEN DATE(?) AND DATE(?)''',
            connection,
            params=(work_place, str(start_date), str(end_date))
        )
        

        if df['montly_hours'].sum() > 0:

            salary = functions.WORKED_COMPANIES.get(f'{work_place}').get('salary')

        else:
            salary = df.get('total_hours').sum() * df.get('salary_per_hour').mean()
        

        cursor.execute(
                    '''UPDATE WorkHours SET payed = 1
                       WHERE company = ? AND DATE(date_of_work) BETWEEN DATE(?) AND DATE(?)''',
                    (work_place, str(start_date), str(end_date))
                )

        connection.commit()

        write_income(work_place, salary, date_of_pay, f'{start_date} - {end_date}')

        functions.proces_logger(f'{work_place} | {start_date}-{end_date} paid', 'DataWork/payed_from_works')

    except Exception as e:
        functions.erro_logger(e, 'DataWork/payed_from_works')


def over_times_per_work(company, hours, nominal, month):

    try:

        corsor = connection.cursor()

        corsor.execute(

            '''
                CREATE TABLE IF NOT EXISTS OverTimes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT,
                hours REAL,
                nominal REAL,
                month TEXT)

            '''
        )        

        corsor.execute('''

            INSERT INTO OverTimes (company, hours, nominal, month)
            VALUES(?,?,?,?)

            ''', (company, hours, nominal, month))

        connection.commit()

    except Exception as e:
        functions.erro_logger(e, 'DataWorks/over_time_per_work')    

# debits

def write_debits(name, amount, deadline,date):

    try:    
        corsor.execute('''

            CREATE TABLE IF NOT EXISTS Debits(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            amount REAL,
            deadline TEXT,
            status INTEGER,
            added_date TEXT)

            ''')

        corsor.execute(f'''

            INSERT INTO Debits(name, amount, deadline, status, added_date)
            Values(?,?,?,?,?)''',(name, amount,  deadline, 0, date)

            )

        connection.commit()

        functions.proces_logger(f'For {name} {amount} EUR added to Debits Table ','DataWork/write_debits' )

    except Exception as e:
        functions.erro_logger(e, 'DataWork/write_debits')


def change_debit_status(iid):

    try:
        corsor.execute('''

                UPDATE Debits
                SET status = 1
                WHERE id = ? 

                ''', (iid,))

        connection.commit()
        
        functions.proces_logger(f'for {iid} of debit status changed', 'functions/change_debit_status')
    except Exception as e:
        functions.erro_logger(e, 'functions/change_debit_status')