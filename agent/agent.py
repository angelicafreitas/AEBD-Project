import requests as req
import json
import cx_Oracle as orc
import config
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

    print('Fetching data...')
    try:
        with orc.connect(USERNAME, PASSWORD, DSN, encoding=ENCODING) as db:
            with db.cursor() as cursor:
                cursor.execute(f'select sysdate from dual')
                res, = cursor.fetchone()
                print(f'\t > {res}\n')
                #TABLESPACES select * from DBA_TABLESPACES;
                #DATA FILES select * from DBA_DATA_FILES;
                
                #CPU usage
                """ SELECT DISTINCT se.username, ss.sid, ROUND (value/100) "CPU Usage"
                FROM v$session se, v$sesstat ss, v$statname st
                WHERE ss.statistic# = st.statistic#
                AND name LIKE  '%CPU used by this session%'
                AND se.sid = ss.SID 
                AND se.username IS NOT NULL
                ORDER BY ss.sid DESC; """

                #Memory usage SGA PGA
                """ SELECT sn.INSTANCE_NUMBER,
                        sga.allo sga,
                        pga.allo pga,
                        (sga.allo + pga.allo) tot,
                        TRUNC (SN.END_INTERVAL_TIME, 'mi') time
                    FROM (  SELECT snap_id,
                                INSTANCE_NUMBER,
                                ROUND (SUM (bytes) / 1024 / 1024 / 1024, 3) allo
                            FROM DBA_HIST_SGASTAT
                        GROUP BY snap_id, INSTANCE_NUMBER) sga,
                        (  SELECT snap_id,
                                INSTANCE_NUMBER,
                                ROUND (SUM (VALUE) / 1024 / 1024 / 1024, 3) allo
                            FROM DBA_HIST_PGASTAT
                            WHERE name = 'total PGA allocated'
                        GROUP BY snap_id, INSTANCE_NUMBER) pga,
                        dba_hist_snapshot sn
                WHERE     sn.snap_id = sga.snap_id
                        AND sn.INSTANCE_NUMBER = sga.INSTANCE_NUMBER
                        AND sn.snap_id = pga.snap_id
                        AND sn.INSTANCE_NUMBER = pga.INSTANCE_NUMBER
                ORDER BY sn.snap_id DESC, sn.INSTANCE_NUMBER; """
    except Exception as e:
        raise e
    print('Data fetched!\n')




elif sys.argv.__len__() > 1 and sys.argv[1] in ['--help', '-h']:
    print('Syntax: agent.py [PORT] [PDB NAME] [USERNAME] [PWD]')    
    exit()

else:
    print('Error: check --help or -h for correct syntax')
    exit()

