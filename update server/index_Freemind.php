<?php
$currenturl = "46.182.19.177:8002";
$vfreemind = "1.0";
$vfreemindbackup = "1.0";
$userversion = $_GET["userversion"];
$userprogram = $_GET["userprogram"];
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
