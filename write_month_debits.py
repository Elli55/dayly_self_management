import pandas as pd
import functions
import DataWork





def debit_exists_this_month(name, connection):

    try:
        df = pd.read_sql('''
            SELECT COUNT(*) as count FROM Debits
            WHERE name = ?
            AND strftime('%Y-%m', added_date) = strftime('%Y-%m', 'now')
            ''', connection, params=(name,))

        return df['count'].iloc[0] > 0

    except Exception as e:
        functions.erro_logger(e, 'recurring/debit_exists_this_month')
        return False


def write_returned_debits():

    today = functions.TODAY

    for item in functions.RECURRING_DEBITS:

        try:
        
            deadline = today.replace(day=item['day'])

           
            if today < deadline:
                continue

            
            if debit_exists_this_month(item['name'], functions.connection):
                continue

            DataWork.write_debits(
                item['name'],
                item['amount'],
                deadline,
                today
            )

            functions.proces_logger(
                f"Recurring debit written: {item['name']} - {item['amount']}",
                'recurring/write_recurring_debits'
            )

        except Exception as e:
            functions.erro_logger(e, 'recurring/write_recurring_debits')