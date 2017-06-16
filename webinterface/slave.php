<!DOCTYPE html>
<html lang="de-DE">

<head>
  <title>FreeMind</title>
  <meta charset="UTF-8" />
  <!-- MEEEIIINNNSSS -->
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans">
  <link rel="shortcut icon" type="image/x-icon" href="img/favicon.ico">
  <link rel="stylesheet" type="text/css" href="css/Meinestyles.css">
  <link rel="stylesheet" type="text/css" href="css/circle.css">
  <!-- Bootstrap -->
  <link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
  <script type="text/javascript" src="js/jquery-3.1.1.min.js"></script>
  <script type="text/javascript" src="js/bootstrap.min.js"></script>
</head>

<body>
  <?php
  function getinfo($variety) {
   // Datenbankdatei öffnen
   $db = new SQLite3("fmweb.db");
   // Abfrage durchführen
   $result = $db->prepare('SELECT content FROM info WHERE client=:client AND variety=:variety');
   $result->bindValue(':client', 2, SQLITE3_INTEGER);
   $result->bindValue(':variety', $variety, SQLITE3_INTEGER);
   $result = $result->execute();
   $data = $result->fetchArray();
   // Verbindung lösen
   $db->close();
   // Ergebnis zurückgeben
   return $data["content"];
  }
  ?>
    <!-- Navbar -->
    <nav class="navbar navbar-default navbar-fixed-top" role="navigation">
        <div class="navbar-header">
            <a class="navbar-brand" href="/">FreeMind</a>
        </div>
        <div>
            <ul class="nav navbar-nav">
                <li><a href="/">Startseite</a></li>
                <li><a href="master.php">Server</a></li>
                <li class="active"><a href="slave.php">Banana Pi</a></li>
                <li><a href="https://github.com/technikamateur/FreeMind/wiki" target="_blank">Handbuch</a></li>
            </ul>
        </div>
    </nav>
    <!-- Jetzt beginnt der eigentliche Spaß -->
    <div id="centerbox2">
        <t2>Systeminformationen:</t2><br><br>
        <div id="firstlistbox">
            <ul class="list-group">
                <li class="list-group-item">
                    <tnormhead>Server Betriebssystem: </tnormhead>
                    <tnorm> Debian Jessie armhf</tnorm>
                </li>
                <li class="list-group-item">
                    <tnormhead>CPU: </tnormhead>
                    <tnorm> Cortex A7 Dual-Core</tnorm>
                </li>
                <li class="list-group-item">
                    <tnormhead>RAM: </tnormhead>
                    <tnorm> 1GB</tnorm>
                </li>
                <li class="list-group-item">
                    <tnormhead>Speicherplatz SD + HDD: </tnormhead>
                    <tnorm> 16GB + 3TB</tnorm>
                </li>
            </ul>
        </div>
        <div id="otherlistbox">
            <ul class="list-group">
                <li class="list-group-item">
                    <tnormhead>Letztes OS-Update: </tnormhead>
                    <tnorm> <?php $content = getinfo(1); echo $content; ?></tnorm>
                </li>
                <li class="list-group-item">
                    <tnormhead>Letztes FreeMind-Update: </tnormhead>
                    <tnorm> <?php $content = getinfo(2); echo $content; ?></tnorm>
                </li>
                <li class="list-group-item">
                    <tnormhead>Letztes Backup: </tnormhead>
                    <tnorm> <?php $content = getinfo(3); echo $content; ?></tnorm>
                </li>
            </ul>
        </div>
    </div>
    <div id="headlinebox">
        <t2>Speicherübersicht:</t2>
        <div id="mainmemoryboxbpi">
            <div id="firstmemorybox">
                <div class="c100 p25 big">
                    <span>25%</span>
                    <div class="slice">
                        <div class="bar"></div>
                        <div class="fill"></div>
                    </div>
                </div>
                <div id="centertextboxmemory">
                    <tmemory>SD-Karte</tmemory>
                </div>
            </div>
            <div id="othermemorybox">
                <div class="c100 p26 big">
                    <span>26%</span>
                    <div class="slice">
                        <div class="bar"></div>
                        <div class="fill"></div>
                    </div>
                </div>
                <div id="centertextboxmemory">
                    <tmemory>HDD-1 (Backup)</tmemory>
                </div>
            </div>
        </div>
    </div>
    <div id="headlineboxundermem">
        <t2> Serveraktionen:</t2>
    </div>
    <div id="serveractions">
        <div class="form-group">
            <label class="sr-only" for="exampleInputPassword3">Password</label>
            <input type="password" class="form-control" id="passwordform" placeholder="Passwort">
        </div>
        <a class="btn btn-default" href="#" role="button">Herunterfahren</a>
        <a class="btn btn-default" href="#" role="button">Neustart</a>
        <a class="btn btn-default" href="#" role="button">Aktualisieren</a>
        <a class="btn btn-default" href="#" role="button">Backup durchfühen</a>
        <a class="btn btn-default" href="#" role="button">Dateisysteme prüfen</a>
        <a class="btn btn-default" href="#" role="button">Festplatte prüfen</a>
    </div>
</body>

</html>
