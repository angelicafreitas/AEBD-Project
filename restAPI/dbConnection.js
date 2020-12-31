var oracledb = require('oracledb');
module.exports = {run}

oracledb.outFormat = oracledb.OUT_FORMAT_OBJECT;

const mypw = "oracle"

async function run(query) {

    let connection;
  
    try {
      connection = await oracledb.getConnection( {
        user          : "c##commonuser",
        password      : mypw,
        connectString : "localhost:1521/aebdpdb.localdomain"
      });
      
    return await connection.execute(query);

    } catch (err) {
      console.error(err);
    } finally {
      if (connection) {
        try {
          await connection.close();
        } catch (err) {
          console.error(err);
        }
      }
    }
  }

