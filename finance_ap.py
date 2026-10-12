import streamlit as st
from streamlit_calendar import calendar
import pandas as pd
import functions
import DataWork
import calculation
import graphics as gp
import write_month_debits
import datetime
from datetime import datetime as dt



try:

    st.set_page_config(page_title='My Space', page_icon='🏃‍♂️‍➡️', layout='wide')

    st.markdown(functions.load_css(), unsafe_allow_html=True) 
    


    if 'page' not in st.session_state:
        st.session_state.page = functions.PAGE_NAMES[0]
except Exception as e:
    functions.erro_logger(e, 'finance_ap.py/start')        





with st.sidebar:
    st.title('Sections')
    st.divider()

    for page_name in functions.PAGE_NAMES:
        is_active = st.session_state.page == page_name
            
        if st.button(
                    page_name,
                    width='stretch',
                    type="primary" if is_active else "secondary"
                    ):
                    
                    st.session_state.page = page_name
                    st.rerun()


page = st.session_state.page


if page == functions.PAGE_NAMES[0]:




    calcol1, calcol2 = st.columns([1,3])

    with calcol1: #input for calendar
        with st.form('WritePlan'):

            st.html("<h1 class='subtitle'> Add Task</h1>")

            titel = st.text_input('Title', placeholder='Brink')
            category = st.selectbox('Category', functions.PLANNER_CATEGORIES)
            date = st.date_input('Date', functions.DATE_OF_DAY)

            time_col1, time_col2 = st.columns(2, gap='xxsmall')

            with time_col1:
                start_time = st.time_input('Start: ', datetime.time(9,0))
            with time_col2:
                end_time = st.time_input('End: ', datetime.time(10,0))

            note = st.text_input('Note', value='')

            if st.form_submit_button('Add'):

                if not titel:
                    st.warning('The title must be written.')
                elif start_time >= end_time:
                    st.warning('There is an error in the adding of times.')
                else:
                    DataWork.add_plan_element(titel, category, date, start_time, end_time, note)
                    st.success(f'{titel} added to {date}')
                    st.rerun()

    with calcol2:  # Calendar

        st.html("<h1 class='subtitle'> Task Board </h1>")

        df_planner = DataWork.df_planner()  

        events = []
        


        for _ , line in df_planner.iterrows():

            color = functions.PLANNER_COLOURS.get(line['category'], '#888888')

            events.append({
                'id': str(line['id']),
                'title': f"{line['title']}",
                'start': f"{line['date']}T{str(line['start'])[:5]}",
                'end':   f"{line['date']}T{str(line['end'])[:5]}",
                'color': color +'40',
                'backgroundcolor':color,
                'extendedProps': {
                    'Category': str(line['category']),
                    'Note': str(line['note']),
                    'Start': str(line['start']),
                    'End': str(line['end']),
                    'db_id': int(line['id'])

                }
            })


        calendar_options = {
            'editable':         False,
            'selectable':       True,
            'initialView':      'dayGridWeek',
            'eventDisplay':     'block',
            'displayEventTime': True,
            'displayEventEnd':  True,
            'eventDisplay': 'block',
            'eventTimeFormat': {'hour': '2-digit', 'minute': '2-digit', 'hour12': False},
            'firstDay':         1,
            'headerToolbar': {
                'left':   'today prev,next',
                'center': 'title',
                'right':  'dayGridMonth,dayGridWeek,listWeek'
            },

            'height': 550
        }   

        calendar_css = """
            
            .fc {
                --fc-border-color: rgba(255, 255, 255, 0.15);
                --fc-today-bg-color: rgba(3, 174, 3, 0.12);
            }

            .fc-daygrid-event.fc-event {
                margin: 0 0.2rem 0.5rem 0.2rem;
                border-width: 3px;
                border-radius: 8px;
            }

            .fc-event-title {
                white-space: pre-line !important;
                font-weight: 700 !important;
                padding: 0.5rem 0 !important;
                word-break: break-word;
                overflow: visible !important;
                text-overflow: clip !important;
                line-height: 1.3;
            }
            .fc-event-time { font-weight: 400 !important; font-size: 0.7rem; margin: 0.5rem 0 !important; }
            .fc-daygrid-event,
            .fc-event-main,
            .fc-event-title-container {
                white-space: normal !important;
                overflow: visible !important;
            }
            .fc-event-main-frame { flex-direction: column; }
            """

        state = calendar(
            events=events,
            options=calendar_options,
            custom_css=calendar_css,
            key='planner_calendar'
        )

        

        if state.get('eventClick'):
            event    = state['eventClick']['event']
            props = event.get('extendedProps', {})
            raw   = event.get('title', '')

            with st.container(border=True):
                col_info, col_del = st.columns([4, 1])
                with col_info:
                    st.html(f"<h1 class='subtitle'> {raw} </h1>")
                    st.caption(f"{str(props.get('Start',''))[:5]} – {str(props.get('End',''))[:5]}")
                    st.caption(props.get('Category', '—'))
                    if props.get('Note') and props.get('Note') not in ('', 'None'):
                        st.caption(props.get('Note'))
                with col_del:
                    if st.button('Delete', key='del_plan', type='secondary', use_container_width=True):
                        DataWork.delete_from_planner(props['db_id'])
                        st.rerun()

    st.divider()

    with st.container(border=True): # Habits Container

        week = []

        for i in range(7):
            week.append(functions.MONDAY + datetime.timedelta(days=i))




        done_list = DataWork.get_done_days()
        monthly = calculation.calculate_monthly_habits()



        colums_habits = ([2] + [1]*8)

        header_of_habits = st.columns(colums_habits)

        header_of_habits[0].html("<p class='subtitle_2'>Habits</p>")

        for i , day in enumerate(week):

            header_of_habits[i +1].html(f"<p class='subtitle_3'>{day.strftime('%a %d')}")

            if i >= 8:
                continue
        header_of_habits[8].html("<p class='subtitle_2'>This Month</p>") 

        for habit in functions.HABITS:

            content_colm_habit = st.columns(colums_habits)

            content_colm_habit[0].html(f"<p class='subtitle'>{habit}</p>")

            if habit in done_list:
                done_day_list = done_list[habit]
            else:
                done_day_list = set()


            for i , day in enumerate(week):

                st_day = str(day)
                is_done = st_day in done_day_list


                is_done_now = content_colm_habit[i + 1].checkbox(
                    f'{habit} {st_day}',
                    value=is_done,
                    key=f'{habit}_{st_day}',
                    label_visibility='collapsed'
                )

                if is_done_now != is_done:
                    DataWork.toggle_habit(habit, day)
                    st.rerun()


                if habit in monthly:
                    total = monthly[habit]
                else:
                    total = 0

            content_colm_habit[8].caption(f'{total} Days')            



    



            

                 
                    





if page == functions.PAGE_NAMES[1]:

    write_month_debits.write_returned_debits()
    

    BALANCE = calculation.calculate_current_balance()
    
    
    last_month_balance, delta_for_balance = calculation.calculate_last_month_balance_and_delta_for_balance()
    sum_this_month_income = calculation.calculate_sum_of_this_month_income()
    last_month_income, delta_for_income = calculation.calculate_last_month_income_and_delta()
    sum_this_month_expenses = calculation.calculate_sum_of_this_month_expense()
    last_month_expenses, delta_for_expenses = calculation.last_month_expenses_and_delta()
    df_debits, df_unpaid_debits, sum_of_unpaid_debits = calculation.df_debits_and_unpaid_debits()
    result_un_paid_salary, total_salary = calculation.un_paid_working_hours()
    
    col1, col2, col3 = st.columns(3, gap='xxsmall')


    with col1:

        st.html(functions.generate_metric_card('Balance', 
                                                BALANCE, delta_for_balance, 
                                                last_month_balance,
                                                higher_is_better=True, 
                                                last_label='Last month avg'))

        
    with col2:

        st.html(functions.generate_metric_card('Income', 
                                                sum_this_month_income, 
                                                delta_for_income, last_month_income,
                                                higher_is_better=True))

    with col3:

        st.html(functions.generate_metric_card('Expenses', 
                                                sum_this_month_expenses, 
                                                delta_for_expenses, 
                                                last_month_expenses,
                                                higher_is_better=False))

    st.divider()

    st.html("<h1 class='title'> This Month Expenses Graphic</h1>")


    fig_expense = gp.generate_graphic_for_expenses_groupby_category()
    if fig_expense is not None:
        st.plotly_chart(fig_expense, width='stretch')
    else:
        st.error('Graphic could not be loaded')

    st.divider()


    st.html("<h1 class='title'> Debits List</h1>")

    
    if df_unpaid_debits.empty:
        st.error('No Debits more')
    else:
        with st.container():
            header_for_debits = st.columns(4, gap='xxsmall')

            header_for_debits[0].html("<p class='df_headers'> The name </p>")
            header_for_debits[1].html("<p class='df_headers'> Amount € </p>")
            header_for_debits[2].html("<p class='df_headers'> Deadline </p>")
            header_for_debits[3].html("<p class='df_headers'> Paid?  </p>")

           

            @st.dialog('Kredits')

            def pay_dialog(line):
                st.markdown(f"**{line['name']}: total kredit - {line['amount']:.2f}")
                st.divider()

                paymet_method = st.radio('Paymet Method', ['Total', 'Partially'], horizontal=True)

                rest = 0.0

                if paymet_method == 'Partially':

                    paid_amout = st.number_input('Amount: ', min_value=0.1,
                                                max_value=float(line['amount']),
                                                step=0.5,
                                                value=float(line['amount']/ 3))
                    rest = round(line['amount'] - paid_amout, 2)
                    st.caption(f'Rest amount : {rest} ')

                else:
                    paid_amout = line['amount']    

                st.divider()

                col1, col2 = st.columns(2)

                if col1.button('Paid', type='primary', width='stretch'):
                    DataWork.write_expenses(line['name'],paid_amout,line['name'],functions.DATE_OF_DAY, f'Paid kreditor for {line['name']}')
                    DataWork.change_debit_status(line['id'])
                    if rest:
                        DataWork.write_debits(line['name'], rest, line['deadline'])

                    st.rerun()

                if col2.button('Out', type='secondary', width='stretch'):
                    st.rerun()


            for _ , row in df_unpaid_debits.iterrows():

                col1, col2, col3, col4 =st.columns(4, gap='xxsmall', )

                col1.html(f"<p class='element_of_df'> {row['name']} </p>")
                col2.html(f"<p class='element_of_df'> {row['amount']} €</p>")
                col3.html(f"<p class='element_of_df'> {row['deadline']} </p>")

                if col4.button('Payed', key=f"pay_{row['id']}"):
                        pay_dialog(row)

            st.html(functions.generate_total_cards(sum_of_unpaid_debits, False))


    st.divider()

    st.html("<h1 class='title'> Working Hours List </h1>")


    if not result_un_paid_salary:
        st.info('No more unpaid working hours')
    else:

        header_for_salary = st.columns(5, gap='xxsmall')

        header_for_salary[0].html("<p class='df_headers'>Company</p>")
        header_for_salary[1].html("<p class='df_headers'>Worked Hours</p>")
        header_for_salary[2].html("<p class='df_headers'>Montly Hours</p>")
        header_for_salary[3].html("<p class='df_headers'>Nominal</p>")
        header_for_salary[4].html("<p class='df_headers'>Salary</p>")

        for item in result_un_paid_salary.items():

            cols = st.columns(5, gap='xxsmall')

            cols[0].html(f"<p class='element_of_df'>{item[0]}</p>")
            cols[1].html(f"<p class='element_of_df'>{item[1].get('worked_hours')}</p>")
            cols[2].html(f"<p class='element_of_df'>{item[1].get('montly_hours')}</p>")
            cols[3].html(f"<p class='element_of_df'>{item[1].get('nominal')}</p>")
            cols[4].html(f"<p class='element_of_df'>{item[1].get('salary')}</p>")

        
        st.html(functions.generate_total_cards(total_salary))

    st.divider()

  

if page == functions.PAGE_NAMES[2]:


    DF_EXPENSES = calculation.load_expenses_df()
    DF_INCOME = calculation.load_income_df()
        

    st.subheader('Input Area')


    col1, col2, col3 =st.columns([5,5,5])

    with col1:
        with st.form('WriteExpense'):
            st.subheader('Write Expenses')
            name_of_expense = st.text_input('Expense name', placeholder='Weekly...', max_chars=50)
            category = st.selectbox('Category', functions.CATEGORY_FOR_EXPENSES )
            amount_of_expense = st.number_input('Amount ', min_value=0.0, max_value=100000.0, step=0.05, value=0.0)
            date_of_expense = st.date_input('Date: ', functions.DATE_OF_DAY)
            note_of_expense = st.text_input('Note : ', value='None')

            if st.form_submit_button('Write'):
                if not name_of_expense:
                    st.warning('Add the NAME pls')
                elif not amount_of_expense:
                    st.warning('add the AMOUNT pls')

                else:
                    DataWork.write_expenses(name_of_expense, amount_of_expense, category,date_of_expense, note_of_expense)
                    st.success(f'{amount_of_expense} - {name_of_expense} added to Expenses Table')

    with col2:

        with st.container(border=True):
            st.subheader('Write Income')
            name_of_income = st.selectbox('Soruce : ', options=functions.INCOME_SOURCE)



            if name_of_income == functions.INCOME_SOURCE[0]:
                            with st.form(f'WriteIncome{functions.INCOME_SOURCE[2]}'):
                                work_place = st.selectbox('Where : ', functions.WORKED_COMPANIES.keys())
                                amoun_of_tip = st.number_input('Amount : ', min_value=0.0, max_value=100000.0, step=1.0)
                                date_of_Tips_taken = st.date_input('Date: ', functions.DATE_OF_DAY)
                                if st.form_submit_button('Write'):
                                    DataWork.write_income(work_place, amoun_of_tip, date_of_Tips_taken,functions.INCOME_SOURCE[2])

            elif name_of_income == functions.INCOME_SOURCE[1]:
                with st.form(f'WriteIncome{functions.INCOME_SOURCE[0]}'):
                    company = st.selectbox('Company : ', functions.WORKED_COMPANIES.keys())
                    from_when = st.date_input('From when : ', functions.DATE_OF_DAY )
                    to_when = st.date_input('To when : ', functions.DATE_OF_DAY )
                    date_of_pay = st.date_input('paid When: ', functions.DATE_OF_DAY)
                    if st.form_submit_button('Write'):
                        DataWork.payed_from_works(company, date_of_pay,from_when, to_when)

            elif  name_of_income == functions.INCOME_SOURCE[2]:
                with st.form(f'WriteIncome{functions.INCOME_SOURCE[1]}'):
                    donor = st.selectbox('Soruce :', functions.DONOR_SCHOLLERSHIPS)
                    amount_from_donor = st.number_input('Amount : ', min_value=0.0 , max_value=10000.0, step=1.0)
                    date_of_stipendium = st.date_input('Date: ', functions.DATE_OF_DAY)
                    if st.form_submit_button('Write'):
                        DataWork.write_income(donor, date_of_stipendium,amount_from_donor,functions.INCOME_SOURCE[1])
                        

            

            elif name_of_income == functions.INCOME_SOURCE[3]:
                with st.form(f'WriteIncome{functions.INCOME_SOURCE[3]}'):
                    from_who = st.text_input('From : ', max_chars=50)
                    amoun_of_debit = st.number_input('Amount : ', max_value=10000.0, min_value=0.0, step=1.0)
                    date_of_taking = st.date_input('Date: ', functions.DATE_OF_DAY)
                    deadline = st.date_input('Deadline : ', functions.DATE_OF_DAY)
                    if st.form_submit_button('Write'):
                        DataWork.write_income(from_who, amoun_of_debit,date_of_taking, functions.INCOME_SOURCE[3])
                        DataWork.write_debits(from_who,amoun_of_debit,deadline,date_of_taking)
            elif name_of_income ==  functions.INCOME_SOURCE[4]:
                with st.form(f'WriteIncome{functions.INCOME_SOURCE[4]}'):
                    type_of_invest = st.selectbox('Which one: ', ['Cash','Coin', 'Crypto'])     
                    amount_from_invest = st.number_input('Amount: ', min_value=0.0, step=1.0)
                    date_of_invest_taken = st.date_input('Date: ', functions.DATE_OF_DAY)
                    if st.form_submit_button('Write'):
                        DataWork.write_income(type_of_invest,amount_from_invest,date_of_invest_taken, functions.INCOME_SOURCE[4])





    with col3:

        with st.form('WriteWorkHours'):
            st.subheader('Write Working Hours')

            company_name    = st.selectbox('Company', functions.WORKED_COMPANIES.keys())
            date_of_work    = st.date_input('Date', value=functions.DATE_OF_DAY)

            col_t1, col_t2 = st.columns(2)
            with col_t1:
                start_time  = st.time_input('Start time', value=datetime.time(12, 0))
            with col_t2:
                end_time    = st.time_input('End time',   value=datetime.time(18, 0))

            salary_per_hour = st.number_input('Salary per hour (€)',
                                            value=14.5, min_value=0.0,
                                            max_value=1000.0, step=0.5)

            
            if start_time and end_time:
                
                diff = round(
                    (dt.combine(datetime.date.today(), end_time) -
                    dt.combine(datetime.date.today(), start_time)
                    ).total_seconds() / 3600, 2
                )
                if diff > 0:
                    st.caption(f'Total: {diff}h × {salary_per_hour} € = {round(diff * salary_per_hour, 2)} €')
                else:
                    st.warning('End time must be after start time')

            if st.form_submit_button('Write'):
                if end_time <= start_time:
                    st.error('End time must be after start time')
                else:
                    DataWork.write_work_hours(
                        company_name, date_of_work,
                        start_time, end_time, salary_per_hour
                    )
                    st.success(f'{diff}h added for {company_name}')



    st.divider()

    st.html("<h1 class='subtitle'> Last 10 Expenses List</h1>")


    with st.container():

        head_of_expense_list = st.columns([3,3,3,3,2])

        head_of_expense_list[0].html("<p class='df_headers'>Name</p>")
        head_of_expense_list[1].html("<p class='df_headers'>Amount</p>")
        head_of_expense_list[2].html("<p class='df_headers'>Date</p>")
        head_of_expense_list[3].html("<p class='df_headers'>Note</p>")
        head_of_expense_list[4].html("<p class='df_headers'>Delete?</p>")

        for _, line in DF_EXPENSES.tail(10).iloc[::-1].iterrows():

            colums = st.columns([3,3,3,3,2])

            colums[0].html(f"<p class='element_of_df'>{line['name']}</p>")
            colums[1].html(f"<p class='element_of_df'>{line['amount']}</p>")
            colums[2].html(f"<p class='element_of_df'>{line['date']}</p>")
            colums[3].html(f"<p class='element_of_df'>{line['note']}</p>")

            if colums[4].button('Delete', key=f'expense_{line['id']}'):
                DataWork.delete_expenses(line['name'], line['date'])
                st.success(f'{line['name']} in {line['date']} deleted')

    st.divider()

    st.html("<h1 class='subtitle'> Last 10 Income List</h1>")

    with st.container():

        head_of_income_list = st.columns([3,3,3,3,2])

        head_of_income_list[0].html("<p class='df_headers'>Source</p>")
        head_of_income_list[1].html("<p class='df_headers'>Amount</p>")
        head_of_income_list[2].html("<p class='df_headers'>Date</p>")
        head_of_income_list[3].html("<p class='df_headers'>Note</p>")
        head_of_income_list[4].html("<p class='df_headers'>Delete?</p>")



        for _, line in DF_INCOME.tail(10).iloc[::-1].iterrows():

            colums = st.columns([3,3,3,3,2])

            colums[0].html(f"<p class='element_of_df'>{line['source']}</p>")
            colums[1].html(f"<p class='element_of_df'>{line['amount']}</p>")
            colums[2].html(f"<p class='element_of_df'>{line['date']}</p>")
            colums[3].html(f"<p class='element_of_df'>{line['note']}</p>")

            if colums[4].button('Delete', key=f'key_{line['id']}'):
                DataWork.delete_income(line['source'], line['date'])
                st.success(f'{line['source']} in {line['date']} deleted')



