-- DROP TABLE memory;
-- DROP TABLE cpu;
-- DROP TABLE datafiles;
-- DROP TABLE tablespaces;
-- DROP TABLE users_privileges;
-- DROP TABLE privileges;
-- DROP TABLE users;
-- DROP TABLE db;

create table db (
  database_name varchar2(200) not null,
  instance_name varchar2(200),
  version varchar2(200),
  CONSTRAINT db_PK PRIMARY KEY (database_name)
);

/*create table sql_monitor (
    sql_monitor_id int not null enable,
    db_id int,
    sql_text varchar2(200),
    pdb varchar2(200),
    query_date timestamp,
    CONSTRAINT SQL_MONITOR_PK PRIMARY KEY (sql_monitor_id),
    CONSTRAINT SQL_MONITOR_FK FOREIGN KEY (db_id) REFERENCES db(db_id)
);*/

create table users (
    user_id int not null enable,
    database_name varchar2(200) not null,
    user_name varchar2(200),
    default_tablespace varchar2(200),
    temporary_tablespace varchar2(200),
    query_date timestamp not null,
    CONSTRAINT USER_PK PRIMARY KEY (user_id,query_date),
    CONSTRAINT USER_FK FOREIGN KEY (database_name) REFERENCES db(database_name)
);

create table privileges (
    privilege_id int not null enable,
    name varchar2(200),
    property int,
    CONSTRAINT PRIVILEGE_PK PRIMARY KEY (privilege_id)
);

create table users_privileges (
    users_privileges_id int not null enable,
    user_id int,
    query_date timestamp,
    privilege_id int,
    CONSTRAINT USERS_PRIVILEGES_PK PRIMARY KEY (users_privileges_id),
    CONSTRAINT USERS_PRIVILEGES_FK1 FOREIGN KEY (user_id, query_date) REFERENCES users(user_id, query_date),
    CONSTRAINT USERS_PRIVILEGES_FK2 FOREIGN KEY (privilege_id) REFERENCES privileges(privilege_id)
);

create table tablespaces (
    tablespace_name varchar2(200) not null enable,
    database_name varchar2(200) not null,
    sizeMB int,
    free int,
    used int,
    temporary number(1),
    query_date timestamp not null,
    CONSTRAINT TABLESPACE_PK PRIMARY KEY (tablespace_name, query_date),
    CONSTRAINT TABLESPACE_FK FOREIGN KEY (database_name) REFERENCES db(database_name)
);

create table datafiles (
    file_id int not null enable,
    file_name varchar2(200),
    tablespace_name varchar2(200) not null,
    sizeMB int,
    free int,
    used int,
    datafiles_query_date timestamp not null,
    query_date timestamp not null,
    CONSTRAINT DATAFILE_PK PRIMARY KEY (file_id,datafiles_query_date),
    CONSTRAINT DATAFILE_FK FOREIGN KEY (tablespace_name,query_date) REFERENCES tablespaces(tablespace_name,query_date)
);

create table cpu (
    stat_name varchar2(200) not null enable,
    database_name varchar2(200) not null,
    value varchar2(200),
    comments varchar2(200),
    query_date timestamp not null,
    CONSTRAINT CPU_PK PRIMARY KEY (stat_name,query_date),
    CONSTRAINT CPU_FK FOREIGN KEY (database_name) REFERENCES db(database_name)
);

create table memory (
    memory_id INT GENERATED ALWAYS as IDENTITY(START with 1 INCREMENT by 1),
    database_name varchar2(200) not null,
    total int not null enable,
    used int,
    query_date timestamp not null ,
    CONSTRAINT MEMORY_PK PRIMARY KEY (memory_id, query_date),
    CONSTRAINT MEMORY_FK FOREIGN KEY (database_name) REFERENCES db(database_name)
);