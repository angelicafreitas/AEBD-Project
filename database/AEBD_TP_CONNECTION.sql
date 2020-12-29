create table db (
  db_id int not null enable,
  database_name varchar2(200),
  instance_name varchar2(200),
  "version" varchar2(200),
  CONSTRAINT db_PK PRIMARY KEY (db_id)
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
    db_id int,
    user_name varchar2(200),
    default_tablespace varchar2(200),
    temporary_tablespace varchar2(200),
    query_date timestamp,
    CONSTRAINT USER_PK PRIMARY KEY (user_id),
    CONSTRAINT USER_FK FOREIGN KEY (db_id) REFERENCES db(db_id)
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
    privilege_id int,
    CONSTRAINT USERS_PRIVILEGES_PK PRIMARY KEY (users_privileges_id),
    CONSTRAINT USERS_PRIVILEGES_FK1 FOREIGN KEY (user_id) REFERENCES users(user_id),
    CONSTRAINT USERS_PRIVILEGES_FK2 FOREIGN KEY (privilege_id) REFERENCES privileges(privilege_id)
);

create table tablespaces (
    tablespace_name varchar2(200) not null enable,
    db_id int,
    sizeMB int,
    free int,
    used int,
    query_date timestamp,
    CONSTRAINT TABLESPACE_PK PRIMARY KEY (tablespace_name),
    CONSTRAINT TABLESPACE_FK FOREIGN KEY (db_id) REFERENCES db(db_id)
);

create table datafiles (
    file_id int not null enable,
    file_name varchar2(200),
    tablespace_name varchar2(200),
    sizeMB int,
    free int,
    used int,
    query_date timestamp,
    CONSTRAINT DATAFILE_PK PRIMARY KEY (file_id),
    CONSTRAINT DATAFILE_FK FOREIGN KEY (tablespace_name) REFERENCES tablespaces(tablespace_name)
);