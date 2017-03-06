#Creating sqlite3 package
sqlite3 = require('sqlite3').verbose()

#Creating a Database instance
db = new (sqlite3.Database)('test.db')
console.log "Successfully connected"

db.serialize ->
  console.log "The contents of the table STUDENT are ::"
  db.each 'SELECT rowid AS id, name,age,city FROM STUDENT', (err, row) ->
    console.log row.id + ': ' +row.name+', '+ row.age+', '+ row.city
    return
  return
db.close()