<!DOCTYPE html>
<html lang="de-DE">

<head>
  <title>FreeMind</title>
  <meta charset="UTF-8" />
  <link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
  <script type="text/javascript" src="js/jquery-3.1.1.min.js"></script>
  <script type="text/javascript" src="js/bootstrap.min.js"></script>
  <link rel="shortcut icon" type="image/png" href="favicon-300px.png">
  <link rel="stylesheet" type="text/css" href="css/fmstyles.css">
  <link rel="stylesheet" type="text/css" href="css/circle.css">
  <link rel="stylesheet" type="text/css" href="css/reflex.min.css">
</head>

<body>
<!-- Get Memory from Database -->
  <?php
  // array erstellen
  $mem = array();
  $name = array();
  $color = array();
  // Datenbankdatei öffnen
  $db = new SQLite3("fmweb.db");
  // Abfrage durchführen
  $res = $db->query("SELECT * FROM memory");
  // Abfrageergebnis verarbeiten
  while($dsatz = $res->fetchArray(SQLITE3_ASSOC))
  {
    array_push($name, $dsatz["name"]);
    array_push($mem, $dsatz["percent"]);
    array_push($color, $dsatz["smart"]);
  }
  // Verbindung lösen
  $db->close();
  ?>
  <?php
  function getinfo($variety) {
   // Datenbankdatei öffnen
   $db = new SQLite3("fmweb.db");
   // Abfrage durchführen
   $result = $db->prepare('SELECT content FROM info WHERE client=:client AND variety=:variety');
   $result->bindValue(':client', 1, SQLITE3_INTEGER);
   $result->bindValue(':variety', $variety, SQLITE3_INTEGER);
   $result = $result->execute();
   $data = $result->fetchArray();
   // Verbindung lösen
   $db->close();
   // Ergebnis zurückgeben
   return $data["content"];
  }
  ?>
  <nav class="navbar navbar-default navbar-fixed-top" role="navigation">
    <div class="navbar-header">
      <a class="navbar-brand" href="index.html">FreeMind</a>
    </div>
    <div>
      <ul class="nav navbar-nav">
        <li><a href="index.html">Startseite</a></li>
        <li class="active"><a href="server.php">Server</a></li>
        <li><a href="bananapi.html">Banana Pi</a></li>
        <li><a href="freemind.pdf">Handbuch</a></li>
      </ul>
    </div>
  </nav>
  <div class="informationbox">
    <f2>Systeminformationen:</f2><br><br>
    <div class="grid">
      <div class="grid__col-4">
        <ul class="list-group">
          <li class="list-group-item">
            <f3>Server Betriebssystem: </f3>
            <f4> Ubuntu Server 16.04 (64bit)</f4>
          </li>
          <li class="list-group-item">
            <f3>CPU: </f3>
            <f4> AMD A4-6300</f4>
          </li>
          <li class="list-group-item">
            <f3>RAM: </f3>
            <f4> 4GB</f4>
          </li>
          <li class="list-group-item">
            <f3>Mainboard: </f3>
            <f4> GA-f3A78M-HD2 (rev. 3.1)</f4>
          </li>
          <li class="list-group-item">
            <f3>Gesamtspeicherplatz: </f3>
            <f4> > 8TB</f4>
          </li>
        </ul>
      </div>
      <div class="grid__col-4">
        <ul class="list-group">
          <li class="list-group-item">
            <f3>Letztes OS-Update: </f3>
            <f4> <?php $content = getinfo(1); echo $content; ?></f4>
          </li>
          <li class="list-group-item">
            <f3>Letztes FreeMind-Update: </f3>
            <f4> <?php $content = getinfo(2); echo $content; ?></f4>
          </li>
          <li class="list-group-item">
            <f3>Letzte Ausführung Papierkorb-Skript: </f3>
            <f4> <?php $content = getinfo(4); echo $content; ?></f4>
          </li>
          <li class="list-group-item">
            <f3>Letztes Backup: </f3>
            <f4> <?php $content = getinfo(3); echo $content; ?></f4>
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div class="memorybox">
    <f2>Speicherübersicht:</f2>
    <div class="memorybox__circles">
      <div class="grid">
        <div class="grid__col-3">
          <div class="c100 p<?php echo $mem[0]; ?> big center <?php echo $color[0]; ?>">
            <span>
              <?php
              echo $mem[0]."%";
              ?>
            </span>
            <div class="slice">
              <div class="bar"></div>
              <div class="fill"></div>
            </div>
          </div>
          <div class="memorybox__description">
            <f5><?php echo $name[0]; ?></f5>
          </div>
        </div>
        <div class="grid__col-3">
          <div class="c100 p<?php echo $mem[1]; ?> big center <?php echo $color[1]; ?>">
            <span>
              <?php
              echo $mem[1]."%";
              ?>
            </span>
            <div class="slice">
              <div class="bar"></div>
              <div class="fill"></div>
            </div>
          </div>
          <div class="memorybox__description">
            <f5><?php echo $name[1]; ?></f5>
          </div>
        </div>
        <div class="grid__col-3">
          <div class="c100 p<?php echo $mem[2]; ?> big center <?php echo $color[2]; ?>">
            <span>
              <?php
              echo $mem[2]."%";
              ?>
            </span>
            <div class="slice">
              <div class="bar"></div>
              <div class="fill"></div>
            </div>
          </div>
          <div class="memorybox__description">
            <f5><?php echo $name[2]; ?></f5>
          </div>
        </div>
        <div class="grid__col-3">
          <div class="c100 p<?php echo $mem[3]; ?> big center <?php echo $color[3]; ?>">
            <span>
              <?php
              echo $mem[3]."%";
              ?>
            </span>
            <div class="slice">
              <div class="bar"></div>
              <div class="fill"></div>
            </div>
          </div>
          <div class="memorybox__description">
            <f5><?php echo $name[3]; ?></f5>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="actionbox">
    <f2> Serveraktionen:</f2>
    <div class="actionbox__actions">
      Jetzt ein grid...
      <p>
        <div class="form-group">
          <label class="sr-only" for="exampleInputPassword3">Password</label>
          <input type="password" class="form-control" id="passwordform" placeholder="Passwort">
        </div>
        <a class="btn btn-default" href="#" role="button">Herunterfahren</a>
        <a class="btn btn-default" href="#" role="button">Neustart</a>
        <a class="btn btn-default" href="#" role="button">Aktualisieren</a>
        <a class="btn btn-default" href="#" role="button">Dateisysteme prüfen</a>
        <a class="btn btn-default" href="#" role="button">Festplatten prüfen</a>
      </p>
    </div>
  </div>
</body>

</html>
