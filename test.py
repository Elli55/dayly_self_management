import datetime
import pandas as pd
import sqlite3 as sq
import calculation
import functions
import DataWork

connection = functions.connection

corsor = connection.cursor()

# corsor.execute('''

#         UPDATE Workhours SET montly_hours=80 WHERE company='BrinkGeherMeyer'

# ''')

# connection.commit()
# df_workhours = pd.read_sql('''

#             SELECT * FROM Workhours
#                 ''', connection)
# print(df_workhours.head())


# grouped_by_company = pd.read_sql('''

#                     SELECT company, sum(total_hours) as worked_hours,
#                     AVG(montly_hours) as montly_hours, 
#                     AVG(salary_per_hour) as nominal  
#                     FROM Workhours 
#                     WHERE payed = 0 GROUP BY company

#                     ''', connection)
# for _ , line in grouped_by_company.iterrows():

#     print(line)

# sum(grouped_by_company.get('salary'))

# df_expenses = pd.read_sql('SELECT * FROM Debits', connection)

# print(df_expenses)


# print(datetime.datetime.now().strftime('%Y.%m.%d'))

# print(datetime.date.today())


# print(calculation.BALANCE)



# print(calculation.calculate_last_month_income_and_delta())

# a = 50
# b = 2500
# print(a / b * 100)

# print(calculation.group_by_the_category_expenses_sum())

# for _, row in calculation.group_by_the_category_expenses_sum().iterrows():
#     print('ikinci:   ' , row)
    

# print(calculation.df_debits_un_paid)
# print(calculation.load_expenses_df())
# print(sum(calculation.load_expenses_df()['amount']))
# print(calculation.df_income)

# print(calculation.df_working)


# DataWork.update_balance()



# for _, line in calculation.un_paid_working_hours().iterrows():
#     print(line)

# print(sum(calculation.un_paid_working_hours()['salary']))

# df_work_hours = pd.read_sql('SELECT * FROM WorkHours', connection)
# print(df_work_hours)


# print(pd.DataFrame())

# companys = functions.WORKED_COMPANIES.keys()

# print(companys)

# company = 'BrinkGeherMeyer'
# x = functions.WORKED_COMPANIES.get(f'{company}').get('montly_hours')
# print(x)

# def nese():

#     a = None

#     return print(a) or print(2)

# nese()



# for _, line in calculation.load_expenses_df().tail(10).iloc[::-1].iterrows():
#     print(line['name'])

# df_work_hours = pd.read_sql('SELECT * FROM WorkHours', connection)

# total_chek = 0
# for _, line in df_work_hours.iterrows():

#     if line['company'] == 'BrinkGeherMeyer':
#         total_chek += line['total_hours']

# print(total_chek) 


# def un_paid_working_hours():

#     df_work_hours = pd.read_sql('SELECT * FROM WorkHours', connection)
#     try:
         
#             grouped_by_company = pd.read_sql('''
         
#                 SELECT company, SUM(total_hours * salary_per_hour)  as salary, SUM(total_hours) as hours, salary_per_hour as nominal  FROM WorkHours
#                 WHERE payed = 0
#                 GROUP BY company
#                 ''', connection)
         
#             sum_of_salary = sum(grouped_by_company['salary'])
         
#             return grouped_by_company, sum_of_salary
         
#     except Exception as e:
#                 functions.erro_logger(e, 'calculation/un_paid_working_hours')
#                 grouped_by_company = pd.DataFrame()
#                 sum_of_salary = 0
#                 return grouped_by_company, sum_of_salary   
          


# def calculate_fix_monthly_salary_from_companies(company,month, salary_hours, nominal):

#     df__monthly = pd.read_sql('''SELECT * FROM WorkHours
#                                 WHERE company = ?
#                                 AND strftime('%m.%Y', date_of_work) = ?  ''',
#                                 connection, params=(company, month))

    

#     working_hours = 0
    
#     for _, line in df__monthly.iterrows():

#         working_hours += line['total_hours']

#     print('Total hours ', working_hours)

#     if working_hours > salary_hours:

#         DataWork.over_times_per_work(company, working_hours-salary_hours, nominal, month )
#         print('Over time wroted')

    

        



# calculate_fix_monthly_salary_from_companies('BrinkGeherMeyer', '09.2026', 20,13)    

    



# df_over_time = pd.read_sql('''SELECT * FROM OverTimes''', connection)

# print(df_over_time)


# df__monthly = pd.read_sql('''SELECT * FROM WorkHours
#                                 WHERE company = ?
#                                 AND strftime('%m.%Y', date_of_work) = ?  ''',
#                                 connection, params=('BrinkGeherMeyer', '09.2026'))

# print(df__monthly.head())


    




# print(datetime.datetime.month.setter('September'))




# grouped_by_company = pd.read_sql('''

#                     SELECT company, sum(total_hours) as worked_hours,
#                     AVG(montly_hours) as montly_hours, 
#                     AVG(salary_per_hour) as nominal  
#                     FROM Workhours WHERE payed = 0 
#                     GROUP BY company

#                     ''', connection)

# result = {}

        
# for _, line in grouped_by_company.iterrows():

#     if line['montly_hours'] > 0:
#         result[line.get('company')] = {'worked_hours':line['worked_hours'],
#                                       'montly_hours':line['montly_hours'],
#                                       'nominal':line['nominal'],
#                                       'salary':functions.WORKED_COMPANIES.get(f'{line.get('company')}').get('salary')}


# for item in result.items():
#     print(item[0], item[1].get('nominal'))
            

# df = pd.read_sql(
#             '''SELECT * FROM WorkHours
#                WHERE company = ? AND DATE(date_of_work) BETWEEN DATE(?) AND DATE(?)''',
#             connection,
#             params=(work_place, str(start_date), str(end_date))
#         )
        

# if df['montly_hours'] > 0:

#     salary = functions.WORKED_COMPANIES.get(f'{work_place}').get('salary')

# else:
#     total_hours = 0
#     nominal = []

#     for _ , line in df.iterrows():
#         total_hours += line['total_hours']
#         nominal.append(line['salary_per_hour'])

#     salary = total_hours * (sum(nominal) / len(nominal) if nominal else 0)    


        



# df = pd.read_sql(
#             '''SELECT * FROM WorkHours''',
#             connection
#         )
        
# for _, line in df.iterrows():
#     print(line)



# import streamlit as st
# from streamlit_calendar import calendar


# calendar_events = [
#     {"title": "Python Dərsi", "start": "2023-10-27T10:00:00", "end": "2023-10-27T12:00:00"},
#     {"title": "Görüş", "start": "2023-10-28T15:00:00", "end": "2023-10-28T16:00:00"},
# ]


# state = calendar(events=calendar_events)


# if state:
#     st.write("Seçilən hadisə:", state)



# df = DataWork.df_planner()

# print(df)

# for i, linj in df.iterrows():
#     print(linj)4

# print('Day:', functions.DATE_OF_DAY, 'week: ', functions.WEEK_DAYS)

# print(functions.TODAY, '  ', functions.MONDAY)
# print(functions.DATE_OF_DAY)


# print(functions.TODAY - datetime.timedelta(days=3))
# print(datetime.date.today().weekday())

# print(pd.read_sql('''SELECT * FROM Todos''', connection))

# corsor.execute('''

#     DELETE FROM Todos
#     ''')

# corsor.execute(''' UPDATE Income
#                    SET note = 'Tips'
#                    WHERE  note = 'Schollership' 

#                 ''')

connection.commit()

def calculate_tips_pre_company(company):

    df_tips = pd.read_sql('''SELECT * FROM Income
                             WHERE note = 'Tips'

                            ''', connection)

    sum = 0
    
    for _, line in df_tips.iterrows():

        if int(line['date'][5]) ==1:
            print(f"{line['date']} - {line['amount']}")
            sum += line['amount']
    print(sum)





    
calculate_tips_pre_company('BrinkGeherMeyer')    