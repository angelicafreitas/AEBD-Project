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

                # Data needed for Table "DB" -----------------------------------
                print(' > Fetching data for table DB...')
                fetch_db_info = """
                    SELECT (select name from V$database) "Database name" ,
                            sys_context('userenv','instance_name') "Instance name",
                            (SELECT version FROM V$INSTANCE) "Version name" 
                    FROM dual
                """
                cursor.execute(fetch_db_info)
                database_name, instance_name, version_name = cursor.fetchone()
                
                print(f'\tDatabase name: {database_name}')
                print(f'\tInstance name: {instance_name}')
                print(f'\tVersion name: {version_name}')


                #Inserting values to AEBDPDB
                try:
                    with orc.connect(config.dest_USERNAME, config.dest_PASSWORD, config.dest_DSN, encoding=ENCODING) as aedbpdb:
                        cursorAEBD = aedbpdb.cursor()
                                            
                        cursorAEBD.execute(f'INSERT INTO DB (database_name, instance_name,version) VALUES (\'{database_name}\',\'{instance_name}\',\'{version_name}\')')
                        aedbpdb.commit()

                        cursorAEBD.execute("""
                            SELECT db_id FROM (
                                SELECT * FROM db ORDER BY db_id DESC
                            ) WHERE ROWNUM = 1""")
                        last_id, = cursorAEBD.fetchone()
                        
                        print(last_id)                           
                except Exception as e:
                    print(f'HELLO {e}')

                            # cursor.execute("""
                            #     SELECT db_id FROM (
                            #         SELECT * FROM db ORDER BY db_id DESC
                            #     ) WHERE ROWNUM = 1""")
                            # last_id, = cursor.fetchone()


                # # Data needed for table "TABLESPACE" -----------------------------------
                # print('\n')
                # print(' > Fetching data for table TABLESPACE...')
                # fetch_tablespace_info = """
                #     SELECT TABLESPACE_NAME "NAME",
                #             Round(TABLESPACE_SIZE * (SELECT VALUE FROM v$parameter v WHERE name = 'db_block_size')/1024/1024,0) "sizeMB",
                #             Round((TABLESPACE_SIZE-USED_SPACE)* (SELECT VALUE FROM v$parameter v WHERE name = 'db_block_size')/1024/1024,0) "free",
                #             Round(USED_SPACE * (SELECT VALUE FROM v$parameter v WHERE name = 'db_block_size')/1024/1024,0) "used",
                #             CURRENT_TIMESTAMP  "query_date"
                #     FROM DBA_TABLESPACE_USAGE_METRICS
                # """
                # cursor.execute(fetch_tablespace_info)
                # for tablespace_name, sizeMB, free, used, query_date in cursor:             
                #     print(f'\tTablespace name: {tablespace_name}')
                #     print(f'\tSize: {sizeMB}')
                #     print(f'\tFree (MB): {free}')
                #     print(f'\tUsed (MB): {used}')
                #     print(f'\tQuery date: {query_date}')
                #     print(f'\t-----')                

                
                
                # # Data needed for Table "DATAFILES" -----------------------------------
                # print('\n')
                # print(' > Fetching data for table DATAFILES...')
                # fetch_datafile_info = """
                #     SELECT  df.FILE_ID "file_id",
                #             Substr(df.file_name,1,80) "file_name",
                #             Substr(df.tablespace_name,1,20) "tablespace_name",
                #             Round(df.bytes/1024/1024,0) "sizeMB",
                #             decode(f.free_bytes,NULL,0,Round(f.free_bytes/1024/1024,0)) "free",
                #             decode(e.used_bytes,NULL,0,Round(e.used_bytes/1024/1024,0)) "used",
                #             CURRENT_TIMESTAMP "query_date"
                #     FROM    DBA_DATA_FILES DF,
                #         (SELECT file_id,
                #                 sum(bytes) used_bytes
                #             FROM dba_extents
                #             GROUP by file_id) E,
                #         (SELECT sum(bytes) free_bytes,
                #                 file_id
                #             FROM dba_free_space
                #             GROUP BY file_id) f
                #     WHERE    e.file_id (+) = df.file_id
                #     AND      df.file_id  = f.file_id (+)
                #     ORDER BY df.tablespace_name,
                #             df.file_name               
                # """                
                # cursor.execute(fetch_datafile_info)
                
                # for file_id, file_name, tablespace_name, sizeMB, free, used, query_date in cursor:
                #     print(f'\tFile id: {file_id}')
                #     print(f'\tFile name: {file_name}')
                #     print(f'\tTablespace name: {tablespace_name}')
                #     print(f'\tSize: {sizeMB}')
                #     print(f'\tFree (MB): {free}')
                #     print(f'\tUsed (MB): {used}')
                #     print(f'\tQuery date: {query_date}')
                #     print(f'\t-----')                
                
                
                
                # # Data needed for Table USERS -----------------------------------
                # print(' > Fetching data for table USERS...')
                # fetch_user_info = """
                #     SELECT USER_ID,
                #             USERNAME,
                #             DEFAULT_TABLESPACE,
                #             TEMPORARY_TABLESPACE,
                #             CURRENT_TIMESTAMP
                #     FROM DBA_USERS
                # """
                # cursor.execute(fetch_user_info)
                
                # for user_id, user_name, default_tablespace, temporary_tablespace, query_date in cursor:
                #     print(f'\tUser id: {user_id}')
                #     print(f'\tUser name: {user_name}')
                #     print(f'\tDefault tablespace: {default_tablespace}')
                #     print(f'\tTemporary tablespace: {temporary_tablespace}')
                #     print(f'\tQuery date: {query_date}')
                #     print(f'\t-----')                
                

                # # Data needed for Table "PRIVILEGES"
                # print(' > Fetching data for table PRIVILEGES...')
                # fetch_privilege_info = """
                #     SELECT PRIVILEGE, NAME, PROPERTY
                #     FROM SYSTEM_PRIVILEGE_MAP         
                # """
                # cursor.execute(fetch_privilege_info)
                
                # for privilege_id, name, property in cursor:
                #     print(f'\tPrivilege id: {privilege_id}')
                #     print(f'\tName: {name}')
                #     print(f'\tProperty: {property}')
                #     print(f'\t-----')                

                # #----------------------------------------------------------------------------------
                
                # # Data needed for Table "USERS_PRIVELEGES"
                # print(' > Fetching data for table USERS_PRIVILEGES...')
                # fetch_user_privileges_info = """
                #     SELECT d1.USER_ID, SYSTEM_PRIVILEGE_MAP.PRIVILEGE "id_priv"
                #     FROM dba_sys_privs d, DBA_USERS d1, SYSTEM_PRIVILEGE_MAP
                #     WHERE d.PRIVILEGE = SYSTEM_PRIVILEGE_MAP.NAME
                #     AND grantee = d1.USERNAME
                # """
                # cursor.execute(fetch_user_privileges_info)
                
                # for user_id, privilege_id in cursor:
                #     print(f'\tUser id: {user_id}')
                #     print(f'\tPrivilege id: {privilege_id}')
                #     print(f'\t-----')                


                # # Data needed for Table CPU -----------------------------------
                # print(' > Fetching data for table CPU...')
                # fetch_CPU_info = """
                #     SELECT STAT_NAME, VALUE, COMMENTS, CURRENT_TIMESTAMP
                #     FROM V$OSSTAT
                #     WHERE ROWNUM < 10
                #     AND STAT_NAME != 'RSRC_MGR_CPU_WAIT_TIME'               
                # """
                # cursor.execute(fetch_CPU_info)

                # for stat_name, value, comments, query_date in cursor:
                #     print(f'\tStat name: {stat_name}')
                #     print(f'\tValue: {value}')
                #     print(f'\tComments: {comments}')
                #     print(f'\tQuery date: {query_date}')
                #     print(f'\t-----')                


            
                # # Data needed for Table MEMORY -----------------------------------
                # print(' > Fetching data for table MEMORY...')
                # fetch_memory_info = """
                #     SELECT T as "TOTAL (MB)", U as "USED (MB)", CURRENT_TIMESTAMP
                #     FROM dual
                #     INNER JOIN (
                #         SELECT Round(sum(pga_max_mem)/1024/1024) "U", 'X' "DUMMY"
                #         FROM v$process
                #     ) "PGA" ON dual.DUMMY = "PGA".DUMMY
                #     INNER JOIN (
                #         SELECT  Round(sum(value)/1024/1024) "T", 'X' "DUMMY"
                #         FROM v$sga
                #     ) "SGA" ON dual.DUMMY = "SGA".DUMMY
                # """
                # cursor.execute(fetch_memory_info)

                # for total, used, query_date in cursor:
                #     print(f'\tTotal (MB): {total}')
                #     print(f'\tUsed (MB): {used}')
                #     print(f'\tQuery date: {query_date}')
                #     print(f'\t-----')                

    except Exception as e:
        raise e


    print('Data fetched!\n')
elif sys.argv.__len__() > 1 and sys.argv[1] in ['--help', '-h']:
    print('Syntax: agent.py [PORT] [PDB NAME] [USERNAME] [PWD]')    
    exit()

else:
    print('Error: check --help or -h for correct syntax')
    exit()



# SQL but it shows more sql than it should
# select v.SQL_FULLTEXT, v.FIRST_LOAD_TIME, v.CON_ID, v.ELAPSED_TIME, v.EXECUTIONS, v.SERVICE, v.PARSING_USER_ID 
# FROM v$sql v
# WHERE v.SERVICE='orclpdb1.localdomain'
# AND v.PARSING_USER_ID!=0
# ORDER BY v.FIRST_LOAD_TIME DESC;
