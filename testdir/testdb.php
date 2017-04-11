<?php
$id = 1
$db = new SQLite3("test.db");
$statement = $db->prepare('SELECT percent FROM memory WHERE id = :id;');
$statement->bindValue(':id', $id);
$result = $statement->execute();
echo $result;
?>
