var express = require('express');
var router = express.Router();
var dbConnection = require('../dbConnection')

//get CPU
router.get('/cpu', function(req, res, next) {
  dbConnection.run('SELECT * FROM CPU')
  .then(data => res.jsonp(data.rows))
  .catch(err => res.status(400).jsonp(err));
});

//get DATAFILES
router.get('/datafiles', function(req, res, next) {
  dbConnection.run('SELECT * FROM DATAFILES')
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
router.get('/memory', function(req, res, next) {
  dbConnection.run('SELECT * FROM MEMORY')
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
router.get('/tablespaces', function(req, res, next) {
  dbConnection.run('SELECT * FROM TABLESPACES')
  .then(data => res.jsonp(data.rows))
  .catch(err => res.status(400).jsonp(err));
});

//get USERS
router.get('/users', function(req, res, next) {
  dbConnection.run('SELECT * FROM USERS')
  .then(data => res.jsonp(data.rows))
  .catch(err => res.status(400).jsonp(err));
});

//get USERS_PRIVILEGES
router.get('/users_privileges', function(req, res, next) {
  dbConnection.run('SELECT * FROM USERS_PRIVILEGES')
  .then(data => res.jsonp(data.rows))
  .catch(err => res.status(400).jsonp(err));
});

module.exports = router;

