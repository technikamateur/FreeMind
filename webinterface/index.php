<?php
$action = $_GET["action"];
if (is_int($action) && $action < 6) {
  $shellex = shell_exec("/var/www/freemind/php-bridge.sh $action");
  echo $shellex;
} else {
  echo "Argument error!";
?>
