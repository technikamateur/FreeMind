<?php
$currenturl = "http://technikamateur.bplaced.net/tidyup";
$latestversion = "1.0";
$userversion = $_GET["userversion"];
if ($latestversion == $userversion)
{
  print "latest-version";
} else {
  print "$currenturl/$latestversion";
}
$requests = file_get_contents('requests.txt');
$requests = intval($requests);
$requests = $requests + 1;
$datei = fopen("requests.txt", "w");
fwrite($datei, $requests);
?>
