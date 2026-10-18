import pandas as pd
import sqlite3 as sq
import functions


connection = functions.connection




#habits 


def calculate_monthly_habits():

    try:

        df = pd.read_sql('''

            SELECT name, COUNT(*) AS total FROM Habits
            WHERE done = 1
            AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now', 'localtime')
            GROUP BY name

            ''', connection)

        result = dict(zip(df['name'], df['total']))

        return result

    except Exception as e:

        functions.erro_logger(e, 'calculation/calculate_monthly_habits')

        

# balances
def calculate_current_balance():
    try:
        income = pd.read_sql(
            'SELECT SUM(amount) as total FROM Income',
            connection
        ).iloc[0, 0] or 0.0

        expenses = pd.read_sql(
            'SELECT SUM(amount) as total FROM Expenses',
            connection
        ).iloc[0, 0] or 0.0

        return round(float(income) - float(expenses), 2)

    except Exception as e:
        functions.erro_logger(e, 'calculation/calculate_current_balance')
        return 0.0


def calculate_last_month_balance_and_delta_for_balance():

    try:

        df_last_month_balance = pd.read_sql('''SELECT avg(balance) as avg_balance FROM Balance 

                        WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now','start of month' ,'-1 month')

                        ''', connection)

        last_month_balance = round(float(df_last_month_balance.iloc[0, 0] or 0), 2)

        return last_month_balance, functions.generate_delta(last_month_balance, calculate_current_balance())

    except Exception as e:
        functions.erro_logger(e, 'calculation/calculate_last_month_balance_and_delta_of_balance')
        
        return 0, None




# expenses

def load_expenses_df():
    return pd.read_sql('SELECT * FROM Expenses', connection)




def calculate_sum_of_this_month_expense():
    try:
        df_expenses_this = pd.read_sql('''SELECT COALESCE(SUM(amount), 0) FROM Expenses
                               WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')''',
                            connection).iloc[0, 0]
        return round(float(df_expenses_this), 2)

    except Exception as e:
        functions.erro_logger(e, 'calculation/calculate_sum_of_this_month_expense')
        return 0.0


def group_by_the_category_expenses_sum():

    try:
        df = pd.read_sql('''SELECT * FROM Expenses
                            WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')''', connection)
        df_grouped_with_cat = df.groupby(by='category')['amount'].sum().sort_values(ascending=False).reset_index()

    except Exception as e:
        functions.erro_logger(e, 'calculation/group_by_the_category_expenses_sum')
        df_grouped_with_cat = None
    return df_grouped_with_cat


def last_month_expenses_and_delta():

    try:
        df_last_month_expenses = pd.read_sql('''

                                SELECT SUM(amount) as sum_amount FROM Expenses
                                WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now','start of month' , '-1 month')

                            ''', connection).iloc[0,0]
        last_month_expenses = round(float(df_last_month_expenses), 2)

        return last_month_expenses, functions.generate_delta(last_month_expenses, calculate_sum_of_this_month_expense())
    
    except Exception as e:
        functions.erro_logger(e, 'calculation/last_month_expenses_and_delta')
        return 0, None


def sum_month_expenses(month):   
    return pd.read_sql('''SELECT COALESCE(SUM(amount), 0) FROM Expenses
                          WHERE strftime('%Y-%m', date) = ?''',
                       connection, params=(month,)).iloc[0, 0]

# income

def load_income_df():

    return pd.read_sql('SELECT * FROM Income', connection)

def calculate_sum_of_this_month_income():
    try:
        df_this_income = pd.read_sql('''SELECT COALESCE(SUM(amount), 0) FROM Income
                               WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')''',
                            connection).iloc[0, 0]
        
        return round(float(df_this_income), 2)

    except Exception as e:
        functions.erro_logger(e, 'calculation/calculate_sum_of_this_month_income')
        return 0.0


def calculate_last_month_income_and_delta():
    try:
        df_last_month_expenses = pd.read_sql('''SELECT COALESCE(SUM(amount), 0) FROM Income
                               WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now','start of month', '-1 month')''',
                            connection).iloc[0, 0]
        last_month_income = round(float(df_last_month_expenses), 2)

        return last_month_income, functions.generate_delta(last_month_income, calculate_sum_of_this_month_income())

    except Exception as e:
        functions.erro_logger(e, 'calculation/calculate_last_month_income_and_delta')
        return 0, None


# debits

def df_debits_and_unpaid_debits():

    try:
        df_debits = pd.read_sql('SELECT * FROM Debits', connection)
        df_debits_un_paid = pd.read_sql('SELECT * FROM Debits WHERE status = 0', connection)
        sum_of_debits =sum(df_debits_un_paid['amount'])
    except  Exception as e:
        functions.erro_logger(e, 'calculation/df_debits_and_unpaid_debits')
        df_debits = None
        df_debits_un_paid = pd.DataFrame()
        sum_of_debits = 0
    return df_debits, df_debits_un_paid, sum_of_debits


# working



def un_paid_working_hours():


    

    try:

        grouped_by_company = pd.read_sql('''

                    SELECT company, sum(total_hours) as worked_hours,
                    AVG(montly_hours) as montly_hours, 
                    AVG(salary_per_hour) as nominal  
                    FROM Workhours WHERE payed = 0 
                    GROUP BY company

                    ''', connection)

        result = {}
        salary = 0

        
        for _, line in grouped_by_company.iterrows():

            if line['montly_hours'] > 0:
                result[line.get('company')] = {'worked_hours':line['worked_hours'],
                                      'montly_hours':line['montly_hours'],
                                      'nominal':line['nominal'],
                                      'salary':functions.WORKED_COMPANIES.get(f'{line.get('company')}').get('salary')}

            else:
                result[line.get('company')] = {'worked_hours':line['worked_hours'],
                                      'montly_hours':line['montly_hours'],
                                      'nominal':line['nominal'],
                                      'salary':line['worked_hours'] * line['nominal']}

            for item in result.items():
                salary += item[1].get('salary')


        return result, salary
    except Exception as e:
        functions.erro_logger(e, 'calculation/un_paid_working_hours')
        grouped_by_company = pd.DataFrame()
        sum_of_salary = 0
        return grouped_by_company, sum_of_salary


