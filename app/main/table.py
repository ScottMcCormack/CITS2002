from flask_table import Table, Col, DatetimeCol, BoolCol
from babel.dates import format_datetime, get_timezone


class BlockchainTable(Table):
    # Class to format the table
    classes = ['table', 'table-striped']
    # Format the table as perth
    perth_dt = format_datetime(format='dd/MM/yyyy HH:mm:ss zzz',
                               tzinfo=get_timezone('Australia/Perth')
                               )

    from_user = Col('From')
    to_user = Col('To')
    amount = Col('Amount')
    timestamp = DatetimeCol('Timestamp', datetime_format=perth_dt)
    nonce = Col('Nonce')
    miner_verify = BoolCol('Transaction Verified')
