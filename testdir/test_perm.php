<?php
$action = $_GET["action"];
if ($action < 5) {
  echo "NANANANANANANANANANANANANANANA BATMAN!";
  $shellex = shell_exec("bash /etc/freemind/testit.sh");
  echo $shellex;
} else {
  echo "Argument error!";
}
?>
