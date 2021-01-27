var express = require('express');
var router = express.Router();
var dbConnection = require('../dbConnection')

//get CPU
router.get('/cpu/:db_name', function(req, res, next) {
  if(req.query.stat){
    dbConnection.run("SELECT * FROM CPU WHERE DATABASE_NAME ='" + req.params.db_name+ "' and STAT_NAME='" +req.query.stat+ "' order by QUERY_DATE desc")
    .then(data => res.jsonp(data.rows))
    .catch(err => res.status(400).jsonp(err));
  }
  else{
    dbConnection.run("SELECT * FROM CPU WHERE DATABASE_NAME ='" + req.params.db_name+ "' order by QUERY_DATE desc")
    .then(data => res.jsonp(data.rows))
    .catch(err => res.status(400).jsonp(err));
  }

});

//get DATAFILES
router.get('/datafiles/:tablespace', function(req, res, next) {
    dbConnection.run("SELECT * FROM DATAFILES WHERE tablespace_name='" + req.params.tablespace + "'")
    .then(data => res.jsonp(data.rows))
    .catch(err => res.status(400).jsonp(err));  
});

//get DB
router.get('/db', function(req, res, next) {
  dbConnection.run('SELECT * FROM DB')
  .then(data => res.jsonp(data.rows))
  .catch(err => res.status(400).jsonp(err));
});

//get MEMORY
router.get('/memory/:db_name', function(req, res, next) {
  dbConnection.run("SELECT * FROM MEMORY WHERE DATABASE_NAME='" + req.params.db_name + "'")
  .then(data => res.jsonp(data.rows))
  .catch(err => res.status(400).jsonp(err));
});

//get PRIVILEGES
router.get('/privileges', function(req, res, next) {
  dbConnection.run('SELECT * FROM PRIVILEGES')
  .then(data => res.jsonp(data.rows))
  .catch(err => res.status(400).jsonp(err));
});

//get TABLESPACES
router.get('/tablespaces/:db_name', function(req, res, next) {
  if(req.query.tablespace && req.query.recent){
    dbConnection.run('SELECT * FROM TABLESPACES WHERE DATABASE_NAME=\'' + req.params.db_name + "\' and tablespace_name='" + req.query.tablespace + "' order by query_date desc FETCH FIRST 1 ROWS ONLY")
    .then(data => res.jsonp(data.rows))
    .catch(err => res.status(400).jsonp(err)) ;      

  }
  else if(req.query.tablespace){
    dbConnection.run('SELECT * FROM TABLESPACES WHERE DATABASE_NAME=\'' + req.params.db_name + "\' and tablespace_name='" + req.query.tablespace + "' order by query_date desc")
    .then(data => res.jsonp(data.rows))
    .catch(err => res.status(400).jsonp(err)) ;      
  }

  else{
    dbConnection.run('SELECT distinct tablespace_name, temporary FROM TABLESPACES WHERE DATABASE_NAME=\'' + req.params.db_name + "\'")
    .then(data => res.jsonp(data.rows))
    .catch(err => res.status(400).jsonp(err)) ;  
  }
});

//get USERS
router.get('/users/:db_name', function(req, res, next) {
  dbConnection.run("SELECT * FROM USERS WHERE DATABASE_NAME=\'"+ req.params.db_name + "\' order by USER_ID")
  .then(data => res.jsonp(data.rows))
  .catch(err => res.status(400).jsonp(err));
});

//get PRIVILEGES FROM USER
router.get('/users_privileges/:user_id', function(req, res, next) {
  dbConnection.run('select priv_name from users_privileges where user_id='+ req.params.user_id)
  .then(data => res.jsonp(data.rows))
  .catch(err => res.status(400).jsonp(err));
});

//get SESSION FROM USER
router.get('/sessions/:user_id', function(req, res, next) {
  dbConnection.run('select * from "session" s where s.user_id= ' + req.params.user_id)
  .then(data => res.jsonp(data.rows))
  .catch(err => res.status(400).jsonp(err));
});

module.exports = router;

