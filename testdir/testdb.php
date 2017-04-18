<?php
/* Datenbankdatei öffnen */
$db = new SQLite3("test.db");
/* Abfrage durchführen */
$res = $db->query("SELECT * from memory");
/* Abfrageergebnis ausgeben */
while($dsatz = $res->fetchArray(SQLITE3_ASSOC))
{
  echo $dsatz["drive"] . ", "
     . $dsatz["percent"]. "<br />";
}
/* Verbindung lösen */
$db->close()
?>
