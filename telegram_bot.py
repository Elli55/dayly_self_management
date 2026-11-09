import requests as rq


def parse_message(text:str):

    parts = text.strip().split()

    if parts[0].lower() == 'income':

        print(parts)


parse_message(' Icome     nese bele sey ')    

