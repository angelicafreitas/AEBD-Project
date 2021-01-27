import requests as req
import json
import cx_Oracle as orc
import config
import sys

# Oracle connection
ENCODING = "UTF-8"
# -----------------

DB = {"database_name": "", "instance_name": "", "version":""}
TABLESPACES = []
DATAFILES = []
USERS = []
PRIVILEGES = []
USERS_PRIVILEGES = []
CPU = []
MEMORY = []
SESSIONS = []

# ----- ARGUMENT VALIDATION -----
if sys.argv.__len__() != 5:
    if sys.argv[1] in ['--help', '-h']:
        print('Syntax: agent.py [PORT] [PDB NAME] [USERNAME] [PWD]')    
        exit()
    else:
        print('Error: check --help or -h for correct syntax')
        exit()

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

# ----- ----- ------


print(f'------------------------------------------------------------')
print('Fetching data...')
try:
    with orc.connect(USERNAME, PASSWORD, DSN, encoding=ENCODING) as db:
        with db.cursor() as cursor:
            # Data needed for Table "DB" -----------------------------------
            print(' > Fetching data for table DB...')
            fetch_db_info = """
                SELECT (select name from V$database) "Database name" ,
                        sys_context('userenv','instance_name') "Instance name",
                        (SELECT version FROM V$INSTANCE) "Version" 
                FROM dual
            """
            cursor.execute(fetch_db_info)
            database_name, instance_name, version = cursor.fetchone()
            
            DB["database_name"]= database_name
            DB["instance_name"]= instance_name
            DB["version"]= version  
    
            #----------------------------------------------------------------------------------


            # Data needed for table "TABLESPACE" (TEMPORARY) ----------------------------------
            print(' > Fetching data for table TABLESPACE(TEMPORARY) ...')
            #Temporary tablespace
            fetch_tablespace_info = """
                SELECT TABLESPACE_NAME,
                        Round(TABLESPACE_SIZE/1024/1024,0) "SIZE",
                        Round(FREE_SPACE/1024/1024,0) "FREE",
                        Round(ALLOCATED_SPACE/1024/1024,0) "USED",
                        1 "TEMPORARY",
                        CURRENT_TIMESTAMP
                FROM DBA_TEMP_FREE_SPACE
            """
            cursor.execute(fetch_tablespace_info)
            for tablespace_name, sizeMB, free, used, temporary, query_date in cursor:   
                tablespace = {
                    "tablespace_name": tablespace_name,
                    "sizeMB": sizeMB,
                    "free": free,
                    "used": used,
                    "temporary": temporary,
                    "query_date": query_date
                }       
                TABLESPACES.append(tablespace)
    
            #----------------------------------------------------------------------------------


            # Data needed for Table "DATAFILES" -----------------------------------
            print(' > Fetching data for table DATAFILES...')
            fetch_datafile_info = """
                SELECT  df.FILE_ID "file_id",
                        Substr(df.file_name,1,80) "file_name",
                        Substr(df.tablespace_name,1,20) "tablespace_name",
                        Round(df.bytes/1024/1024,0) "sizeMB",
                        decode(f.free_bytes,NULL,0,Round(f.free_bytes/1024/1024,0)) "free",
                        decode(e.used_bytes,NULL,0,Round(e.used_bytes/1024/1024,0)) "used",
                        0 "TEMPORARY",
                        CURRENT_TIMESTAMP "query_date"
                FROM    DBA_DATA_FILES DF,
                    (SELECT file_id,
                            sum(bytes) used_bytes
                        FROM dba_extents
                        GROUP by file_id) E,
                    (SELECT sum(bytes) free_bytes,
                            file_id
                        FROM dba_free_space
                        GROUP BY file_id) f
                WHERE    e.file_id (+) = df.file_id
                AND      df.file_id  = f.file_id (+)
                ORDER BY df.tablespace_name,
                        df.file_name               
            """                
            cursor.execute(fetch_datafile_info)
            
            for file_id, file_name, tablespace_name, sizeMB, free, used, temporary, query_date in cursor:
                datafile = {
                    "file_id": file_id,
                    "file_name": file_name,
                    "tablespace_name": tablespace_name,
                    "sizeMB": sizeMB,
                    "free": free,
                    "used": used,
                    "temporary": temporary,
                    "query_date": query_date                    
                }
                tablespace = {
                    "tablespace_name": tablespace_name,
                    "sizeMB": sizeMB,
                    "free": free,
                    "used": used,
                    "temporary": temporary,
                    "query_date": query_date                    
                }
                TABLESPACES.append(tablespace)
                DATAFILES.append(datafile)
    
            #----------------------------------------------------------------------------------


            # Data needed for Table USERS --------------------------------------------------
            print(' > Fetching data for table USERS...')
            fetch_user_info = """
                SELECT USER_ID,
                        USERNAME,
                        DEFAULT_TABLESPACE,
                        TEMPORARY_TABLESPACE
                FROM DBA_USERS
            """
            cursor.execute(fetch_user_info)
            for user_id, user_name, default_tablespace, temporary_tablespace in cursor:
                user = {
                    "user_id": user_id,
                    "user_name": user_name,
                    "default_tablespace": default_tablespace,
                    "temporary_tablespace": temporary_tablespace
                }
                USERS.append(user)                
    
            #----------------------------------------------------------------------------------


            # Data needed for table PRIVILEGES ------------------------------------------------
            print(' > Fetching data for table PRIVILEGES...')
            fetch_privilege_info = """
                SELECT PRIVILEGE, NAME, PROPERTY
                FROM SYSTEM_PRIVILEGE_MAP         
            """
            cursor.execute(fetch_privilege_info)
            
            for privilege_id, name, property in cursor:
                privilege = {
                    "privilege_id": privilege_id,
                    "name": name,
                    "property": property
                }
                PRIVILEGES.append(privilege)                
    
            #----------------------------------------------------------------------------------


            # Data needed for Table "USERS_PRIVELEGES"
            print(' > Fetching data for table USERS_PRIVILEGES...')
            fetch_user_privileges_info = """
                SELECT d1.USER_ID, SYSTEM_PRIVILEGE_MAP.PRIVILEGE "id_priv"
                FROM dba_sys_privs d, DBA_USERS d1, SYSTEM_PRIVILEGE_MAP
                WHERE d.PRIVILEGE = SYSTEM_PRIVILEGE_MAP.NAME
                AND grantee = d1.USERNAME
            """
            cursor.execute(fetch_user_privileges_info)
            
            for user_id, privilege_id in cursor:
                user_priv ={
                    "user_id": user_id,
                    "privilege_id": privilege_id
                }
                USERS_PRIVILEGES.append(user_priv)
    

            # Data needed for Table CPU -----------------------------------
            print(' > Fetching data for table CPU...')
            fetch_CPU_info = """
                SELECT STAT_NAME, VALUE, COMMENTS, CURRENT_TIMESTAMP
                FROM V$OSSTAT
                WHERE ROWNUM < 10
                AND STAT_NAME != 'RSRC_MGR_CPU_WAIT_TIME'               
            """
            cursor.execute(fetch_CPU_info)
            for stat_name, value, comments, query_date in cursor:
                cpu = {
                    "stat_name": stat_name,
                    "value": value,
                    "comments": comments,
                    "query_date": query_date
                }
                CPU.append(cpu)
    
        
            # Data needed for Table MEMORY -----------------------------------
            print(' > Fetching data for table MEMORY...')
            fetch_memory_info = """
                SELECT T as "TOTAL (MB)", U as "USED (MB)", CURRENT_TIMESTAMP
                FROM dual
                INNER JOIN (
                    SELECT Round(sum(pga_max_mem)/1024/1024) "U", 'X' "DUMMY"
                    FROM v$process
                ) "PGA" ON dual.DUMMY = "PGA".DUMMY
                INNER JOIN (
                    SELECT  Round(sum(value)/1024/1024) "T", 'X' "DUMMY"
                    FROM v$sga
                ) "SGA" ON dual.DUMMY = "SGA".DUMMY
            """
            cursor.execute(fetch_memory_info)
            for total, used, query_date in cursor:
                memory = {
                    "total":total,
                    "used":used,
                    "query_date": query_date
                }
                MEMORY.append(memory)

            # Data needed for table SESSIONS ------------------------------------------------
            print(' > Fetching data for table SESSIONS...')
            fetch_session_info = """
                SELECT SID, USER#, STATUS, LOGON_TIME, LAST_CALL_ET, CURRENT_TIMESTAMP 
                FROM v$session
            """
            cursor.execute(fetch_session_info)
            
            for session_id, user_id, status, longon_time, last_call_et, query_date in cursor:
                session = {
                    "session_id": session_id,
                    "user_id": user_id,
                    "session_status": status,
                    "logon_time": longon_time,
                    "last_call_et": last_call_et,
                    "query_date": query_date
                }
                SESSIONS.append(session)                
            #----------------------------------------------------------------------------------

            print(f'data fetched!')
except Exception as e:
    raise e
print(f'------------------------------------------------------------\n')


print(f'------------------------------------------------------------')
#Inserting values to AEBDPDB
try:
    with orc.connect(config.dest_USERNAME, config.dest_PASSWORD, config.dest_DSN, encoding=ENCODING) as aedbpdb:
        cursorAEBD = aedbpdb.cursor()
        
        print(f'Inserting values to AEBDPDB...')

        #Changing timestamp format to contain fractional numbers
        cursorAEBD.execute('ALTER SESSION SET NLS_TIMESTAMP_FORMAT = \'YYYY-MM-DD HH:MI:SS.FF\'')
        aedbpdb.commit()

        cursorAEBD = aedbpdb.cursor()
        #Checking if db is already in DB
        cursorAEBD.execute(f'select count(1) as total from db\n'
                            f'where DATABASE_NAME= \'{DB["database_name"]}\'')
        total, = cursorAEBD.fetchone()
        
        if total == 1:
            print(f'\tDatabase already in table DB!')
        else:
            #populating table DB
            print(f' > Database isn\'t in table DB')
            print(f' > Populating table DB...')                         
            cursorAEBD.execute(f'INSERT INTO DB (database_name, instance_name,version)\n'
                                f'VALUES (\'{DB["database_name"]}\',\'{DB["instance_name"]}\',\'{DB["version"]}\')')
            aedbpdb.commit()
    
        #populating table TABLESPACES
        cursorAEBD = aedbpdb.cursor()
        print(f' > Populating table TABLESPACES...')
        for tablespace in TABLESPACES:  
            tablespace_timestamp = f'(SELECT TO_TIMESTAMP (\'{tablespace["query_date"]}\', \'YYYY-MM-DD HH24:MI:SS.FF6\') FROM dual)'
            cursorAEBD.execute(f'INSERT INTO TABLESPACES (tablespace_name,database_name, sizemb,free, used, temporary, query_date)\n'
                            f'VALUES (\'{tablespace["tablespace_name"]}\',\'{DB["database_name"]}\',{tablespace["sizeMB"]},{tablespace["free"]},{tablespace["used"]},{tablespace["temporary"]},{tablespace_timestamp})')
        aedbpdb.commit()

        #populating table DATAFILES
        cursorAEBD = aedbpdb.cursor()
        print(f' > Populating table DATAFILES...')
        for datafile in DATAFILES: 
            cursorAEBD.execute(f'SELECT count(1) from datafiles where file_id={datafile["file_id"]}')
            total, = cursorAEBD.fetchone()

            timestamp = f'(SELECT TO_TIMESTAMP (\'{datafile["query_date"]}\', \'YYYY-MM-DD HH24:MI:SS.FF6\') FROM dual)'
            
            if total == 0: 
                cursorAEBD.execute(f'INSERT INTO DATAFILES (file_id, file_name, tablespace_name, sizeMB, free, used, query_date)\n'
                                f'VALUES ({datafile["file_id"]},\'{datafile["file_name"]}\',\'{datafile["tablespace_name"]}\',{datafile["sizeMB"]},{datafile["free"]},{datafile["used"]},{timestamp})')
            else: 
                cursorAEBD.execute(f'UPDATE DATAFILES\n'
                                f'SET file_name=\'{datafile["file_name"]}\',tablespace_name=\'{datafile["tablespace_name"]}\',sizeMB={datafile["sizeMB"]},free={datafile["free"]},used={datafile["used"]}\n'
                                f'WHERE file_id={datafile["file_id"]}')

        aedbpdb.commit()

        #populating table USERS
        cursorAEBD = aedbpdb.cursor()
        print(f' > Populating table USERS...')
        for user in USERS:  
            #Checking if user is already in USERS
            cursorAEBD.execute(f'select count(1) as total from USERS\n'
                                f'where USER_ID= {user["user_id"]}')
            total, = cursorAEBD.fetchone()
            
            if total == 0:
                cursorAEBD.execute(f'INSERT INTO USERS (user_id, database_name, user_name, default_tablespace, temporary_tablespace)\n'
                               f'VALUES ({user["user_id"]},\'{DB["database_name"]}\',\'{user["user_name"]}\',\'{user["default_tablespace"]}\',\'{user["temporary_tablespace"]}\')')
        aedbpdb.commit()



        #populating table PRIVILEGES
        cursorAEBD = aedbpdb.cursor()
        #Checking if there are privileges in PRIVILEGES            
        cursorAEBD.execute(f'SELECT count(1)FROM PRIVILEGES\n')
        total, = cursorAEBD.fetchone()
        
        if total == 0:
            print(f' > Populating table PRIVILEGES...')
            for privilege in PRIVILEGES:  
                cursorAEBD.execute(f'INSERT INTO PRIVILEGES (privilege_id, name, property)\n'
                               f'VALUES ({privilege["privilege_id"]},\'{privilege["name"]}\',{privilege["property"]})')
        aedbpdb.commit()


        #populating table USERS_PRIVILEGES
        cursorAEBD = aedbpdb.cursor()
        print(f' > Populating table USERS_PRIVILEGES...')
        for user_priv in USERS_PRIVILEGES:  
            #Checking if user_priv is already in USERS_PRIVILEGES
            cursorAEBD.execute(f'SELECT count(1) from USERS_PRIVILEGES where user_id={user_priv["user_id"]} and PRIVILEGE_ID={user_priv["privilege_id"]}')
            total, = cursorAEBD.fetchone()
            
            if total == 0:
                cursorAEBD.execute(f'INSERT INTO USERS_PRIVILEGES (user_id, privilege_id)\n'
                               f'VALUES ({user_priv["user_id"]},{user_priv["privilege_id"]})')
        aedbpdb.commit()



        #populating table CPU
        cursorAEBD = aedbpdb.cursor()
        print(f' > Populating table CPU...')
        for cpu in CPU:  
            timestamp = f'(SELECT TO_TIMESTAMP (\'{cpu["query_date"]}\', \'YYYY-MM-DD HH24:MI:SS.FF6\') FROM dual)'
            cursorAEBD.execute(f'INSERT INTO CPU (stat_name,database_name, value, comments, query_date)\n'
                            f'VALUES (\'{cpu["stat_name"]}\',\'{DB["database_name"]}\',\'{cpu["value"]}\',\'{cpu["comments"]}\',{timestamp})')
        aedbpdb.commit()


        #populating table MEMORY
        cursorAEBD = aedbpdb.cursor()
        print(f' > Populating table MEMORY...')
        for memory in MEMORY:  
            timestamp = f'(SELECT TO_TIMESTAMP (\'{memory["query_date"]}\', \'YYYY-MM-DD HH24:MI:SS.FF6\') FROM dual)'
            cursorAEBD.execute(f'INSERT INTO MEMORY (database_name, total, used, query_date)\n'
                            f'VALUES (\'{DB["database_name"]}\', {memory["total"]},{memory["used"]},{timestamp})')
        aedbpdb.commit()

        
        #populating table "session"
        cursorAEBD = aedbpdb.cursor()
        print(f' > Populating table "session"...')
        for session in SESSIONS:  
            cursorAEBD.execute(f'SELECT count(1) from "session" s where s.session_id={session["session_id"]}')
            total, = cursorAEBD.fetchone()
            
            logon= f'(SELECT TO_DATE(\'{session["logon_time"]}\', \'YYYY-MM-DD HH24:MI:SS\') FROM dual)'
            
            if total == 0:
                cursorAEBD.execute(f'INSERT INTO "session" (session_id, user_id,session_status,logon_time, last_call_et)\n'
                                f'VALUES ({session["session_id"]}, {session["user_id"]},\'{session["session_status"]}\',{logon},{session["last_call_et"]})')
            else:
                cursorAEBD.execute(f'UPDATE "session" \n'
                                f'SET user_id = {session["user_id"]}, session_status = \'{session["session_status"]}\', logon_time= {logon}, last_call_et={session["last_call_et"]}\n'
                                f'WHERE session_id= {session["session_id"]}')
        aedbpdb.commit()

        print(f'------------------------------------------------------------')
except Exception as e:
    print(f'HELLO {e}')



