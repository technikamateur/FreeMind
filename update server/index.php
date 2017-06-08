<?php
/* Voreinstellungen */
$ready = True;
$url = "update.freemind-client.org";
$vMaster = 1.0;
$vSlave = 1.0;
$vBetaMaster = 1.0;
$vBetaSlave = 1.0;
/* Parameter empfangen */
$userVersion = $_GET["userVersion"];
$userProgram = $_GET["userProgram"];/* 1=master, 2=slave */
$userChannel = $_GET["userChannel"];/* 1=stable, 2=beta */
/* Parameter prüfen */
if (isset($userVersion) and isset($userProgram) and isset($userChannel)) {
  if (is_numeric($userVersion) && is_numeric($userProgram) && is_numeric($userChannel)) {
    # Nichts tun ...
  } else {
    echo "Argument Error!";
    echo "<br/>";
    echo "Numeric arguments only!";
    $ready = False;
  }
} else {
  echo "Argument Error!";
  $ready = False;
}
/* Ausgabe des Ergebnisses */
if ($ready == True) {
  if ($userChannel == 1) {
    if ($userProgram == 1) {
      if ($userVersion == $vMaster) {
        echo "latest-version";
      } else {
        echo "$url/stable/latest/master.tar.gz";
      }
    } else {
      if ($userVersion == $vSlave) {
        echo "latest-version";
      } else {
        echo "$url/stable/latest/slave.tar.gz";
      }
    }
  } else {
    if ($userProgram == 1) {
      if ($userVersion == $vBetaMaster) {
        echo "latest-version";
      } else {
        echo "$url/beta/latest/master.tar.gz";
      }
    } else {
      if ($userVersion == $vBetaSlave) {
        echo "latest-version";
      } else {
        echo "$url/beta/latest/slave.tar.gz";
      }
    }
  }
}
?>
