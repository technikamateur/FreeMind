<?php
/* Voreinstellungen */
$ready = True;
$url = "31.185.110.8:8002";
$vMaster = 1.0;
$vSlave = 1.0;
$vBetaMaster = 1.0;
$vBetaSlave = 1.0;
/* Parameter empfangen */
$userVersion = $_GET["userVersion"];
$userProgram = $_GET["userProgram"];
$userChannel = $_GET["userChannel"];
/* Parameter prüfen */
if (isset($userVersion) and isset($userProgram) and isset($userChannel)) {
  # Do nothing
} else {
  $ready = False;
}
Jetzt noch in Numern bzw. Text umwandeln (natürlich mit try except und $ready anpassen)
Dann das unten überarbeiten.




if ($userprogram == "freemind") {
  if ($userversion == $vfreemind) {
    print "latest-version";
  } else {
    print "$currenturl/freemind/$vfreemind";
  }
} elseif ($userprogram == "freemind-backup") {
  if ($userversion == $vfreemindbackup) {
    print "latest-version";
  } else {
    print "$currenturl/freemind-backup/$vfreemindbackup";
  }
}
?>
