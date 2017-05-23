<?php
$action = $_GET["action"]; /* 1=OS-Update; 2=FM-Update; 3=Backup-done; 4=Do-Backup? */
if (is_int($action) && $action < 5) {
  $shellex = shell_exec("/etc/freemind/fm_slave_bridge.py $action");
  echo $shellex;
} else {
  echo "Argument error!";
?>
