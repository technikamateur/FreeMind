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
?>
