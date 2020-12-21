import requests as req
import json
import cx_Oracle as orc
import sys

# Oracle connection
ENCODING = "UTF-8"
# -----------------


# ----- ARGUMENT VALIDATION -----
if sys.argv.__len__() == 5:
    try: 
        PORT = int(sys.argv[1])
        DSN = "localhost:"+ sys.argv[1] + "/" + sys.argv[2] + ".localdomain"
        USERNAME = sys.argv[3]
        PASSWORD = sys.argv[4]
        print(f'------------------------------------------------------------')
        print(f'Port: {PORT}')
        print(f'DSN: {DSN}')
        print(f'Username: {USERNAME}')
        print(f'Password: {PASSWORD}')
        print(f'------------------------------------------------------------\n')
    
    except Exception:
        print('Wrong data type')
        exit()

    try:
        with orc.connect(USERNAME, PASSWORD, DSN, encoding=ENCODING) as db:
            with db.cursor() as cursor:
                cursor.execute(f'select sysdate from dual')
                res, = cursor.fetchone()
                print(res)
                #TABLESPACES select * from DBA_TABLESPACES;
                #DATA FILES select * from DBA_DATA_FILES;

    except Exception as e:
        raise e




elif sys.argv.__len__() > 1 and sys.argv[1] in ['--help', '-h']:
    print('Syntax: agent.py [PORT] [PDB NAME] [USERNAME] [PWD]')    
    exit()

else:
    print('Error: check --help or -h for correct syntax')
    exit()

