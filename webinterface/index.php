<?php
$action = $_GET["action"];
if (is_int($action) && $action < 6) {
  $shellex = shell_exec("/etc/freemind/fmmain.py 2 $action");
  echo $shellex;
} else {
  echo "Argument error!";
?>
