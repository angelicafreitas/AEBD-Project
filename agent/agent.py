import requests as req
import json
import cx_Oracle as orc
import config
import sys

# Oracle connection
ENCODING = "UTF-8"
# -----------------


# ----- ARGUMENT VALIDATION -----
# if sys.argv.__len__() == 5:
#     try: 
#         PORT = int(sys.argv[1])
#         DSN = "localhost:"+ sys.argv[1] + "/" + sys.argv[2] + ".localdomain"
#         USERNAME = sys.argv[3]
#         PASSWORD = sys.argv[4]
    
#         print(f'------------------------------------------------------------')
#         print(f'Port: {PORT}')
#         print(f'DSN: {DSN}')
#         print(f'Username: {USERNAME}')
#         print(f'Password: {PASSWORD}')
#         print(f'------------------------------------------------------------\n')
    
#     except Exception:
#         print('Wrong data type')
#         exit()

#     print('Fetching data...')
#     try:
#         with orc.connect(USERNAME, PASSWORD, DSN, encoding=ENCODING) as db:
#             with db.cursor() as cursor:
#                 cursor.execute(f'select sysdate from dual')
#                 res, = cursor.fetchone()
#                 print(f'\t > {res}\n')

#                 # select v.SQL_FULLTEXT, v.FIRST_LOAD_TIME, v.CON_ID, v.ELAPSED_TIME, v.EXECUTIONS, v.SERVICE, v.PARSING_USER_ID 
#                 # FROM v$sql v
#                 # WHERE v.SERVICE='orclpdb1.localdomain'
#                 # AND v.PARSING_USER_ID!=0
#                 # ORDER BY v.FIRST_LOAD_TIME DESC;

#                 #Data needed for tablespace -----------------------------------
#                 # SELECT TABLESPACE_NAME "NAME",
#                 #         Round(TABLESPACE_SIZE * (SELECT VALUE FROM v$parameter v WHERE name = 'db_block_size')/1024/1024,0) "Size (M)",
#                 #         Round((TABLESPACE_SIZE-USED_SPACE)* (SELECT VALUE FROM v$parameter v WHERE name = 'db_block_size')/1024/1024,0) "FREE (M)",
#                 #         Round(USED_SPACE * (SELECT VALUE FROM v$parameter v WHERE name = 'db_block_size')/1024/1024,0) "USED (M)",
#                 #         CURRENT_TIMESTAMP  
#                 # FROM DBA_TABLESPACE_USAGE_METRICS;

#                 #Data needed for datafiles -----------------------------------
#                 # SELECT  df.FILE_ID,
#                 #         Substr(df.file_name,1,80) "File Name",
#                 #         Substr(df.tablespace_name,1,20) "Tablespace Name",
#                 #         Round(df.bytes/1024/1024,0) "Size (M)",
#                 #         decode(f.free_bytes,NULL,0,Round(f.free_bytes/1024/1024,0)) "Free (M)",
#                 #         decode(e.used_bytes,NULL,0,Round(e.used_bytes/1024/1024,0)) "Used (M)",
#                 #         CURRENT_TIMESTAMP
#                 # FROM    DBA_DATA_FILES DF,
#                 #     (SELECT file_id,
#                 #             sum(bytes) used_bytes
#                 #         FROM dba_extents
#                 #         GROUP by file_id) E,
#                 #     (SELECT sum(bytes) free_bytes,
#                 #             file_id
#                 #         FROM dba_free_space
#                 #         GROUP BY file_id) f
#                 # WHERE    e.file_id (+) = df.file_id
#                 # AND      df.file_id  = f.file_id (+)
#                 # ORDER BY df.tablespace_name,
#                 #         df.file_name;
                
#                 # Data needed for Users -----------------------------------
#                 # SELECT USER_ID, USERNAME, DEFAULT_TABLESPACE, TEMPORARY_TABLESPACE, CURRENT_TIMESTAMP
#                 # FROM DBA_USERS;

#                 # All privleges
#                 # SELECT PRIVILEGE, NAME
#                 # FROM SYSTEM_PRIVILEGE_MAP;              
                
#                 # All privileges from Users
#                 # SELECT d1.USERNAME, d.GRANTEE, d.PRIVILEGE, CURRENT_TIMESTAMP 
#                 # FROM dba_sys_privs d, DBA_USERS d1   
#                 # WHERE grantee = d1.USERNAME
#                 # OR grantee in (
#                 #     SELECT granted_role 
#                 #     FROM dba_role_privs 
#                 #     CONNECT BY PRIOR granted_role = grantee 
#                 #     START WITH grantee = d1.USERNAME
#                 # ) ORDER BY 1;              



#                 # Data needed for Info -----------------------------------
#                 # SELECT (SELECT sys_context('userenv','instance_name') FROM dual) "Instance name" , (select name from V$database) "Database name" , (SELECT version FROM V$INSTANCE) "Version name" FROM dual;                


#                 # Data needed for CPU -----------------------------------
#                 # SELECT STAT_NAME, VALUE, COMMENTS, CURRENT_TIMESTAMP
#                 # FROM V$OSSTAT
#                 # WHERE ROWNUM < 10
#                 # AND STAT_NAME != 'RSRC_MGR_CPU_WAIT_TIME';                
                

#                 # Data needed for Memory -----------------------------------
#                 # SELECT T as "TOTAL (MB)", U as "USED (MB)", CURRENT_TIMESTAMP
#                 # FROM dual
#                 # INNER JOIN (
#                 #     SELECT sum(pga_max_mem)/1024/1024 "U", 'X' "DUMMY"
#                 #     FROM v$process
#                 # ) "PGA" ON dual.DUMMY = "PGA".DUMMY
#                 # INNER JOIN (
#                 #     SELECT  sum(value)/1024/1024 "T", 'X' "DUMMY"
#                 #     FROM v$sga
#                 # ) "SGA" ON dual.DUMMY = "SGA".DUMMY;

                
#     except Exception as e:
#         raise e
#     print('Data fetched!\n')
# elif sys.argv.__len__() > 1 and sys.argv[1] in ['--help', '-h']:
#     print('Syntax: agent.py [PORT] [PDB NAME] [USERNAME] [PWD]')    
#     exit()

# else:
#     print('Error: check --help or -h for correct syntax')
#     exit()


#Inserting values to AEBDPDB
try:
    with orc.connect(config.dest_USERNAME, config.dest_PASSWORD, config.dest_DSN, encoding=ENCODING) as aedbpdb:
        with aedbpdb.cursor() as cursor:
            cursor.execute(f'select sysdate from dual')
            res, = cursor.fetchone()
            print(f'> From AEBDPDB {res}')
except Exception as e:
    print(e)