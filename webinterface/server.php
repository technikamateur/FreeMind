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
  <!-- Get Memory from Database -->
  <?php
  /* array erstellen */
  $mem = array();
  $name = array();
  $color = array();
  /* Datenbankdatei öffnen */
  $db = new SQLite3("fmweb.db");
  /* Abfrage durchführen */
  $res = $db->query("SELECT * FROM memory");
  /* Abfrageergebnis verarbeiten */
  while($dsatz = $res->fetchArray(SQLITE3_ASSOC))
  {
    array_push($name, $dsatz["name"]);
    array_push($mem, $dsatz["percent"]);
    array_push($color, $dsatz["smart"]);
  }
  /* Verbindung lösen */
  $db->close();
  ?>
    <!-- Navbar -->
    <nav class="navbar navbar-default navbar-fixed-top" role="navigation">
        <div class="navbar-header">
            <a class="navbar-brand" href="index.html">FreeMind</a>
        </div>
        <div>
            <ul class="nav navbar-nav">
                <li><a href="index.html">Startseite</a></li>
                <li class="active"><a href="server.html">Server</a></li>
                <li><a href="bananapi.html">Banana Pi</a></li>
                <li><a href="freemind.pdf">Handbuch</a></li>
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
                    <tnorm> Ubuntu Server 16.04 (64bit)</tnorm>
                </li>
                <li class="list-group-item">
                    <tnormhead>CPU: </tnormhead>
                    <tnorm> AMD A4-6300</tnorm>
                </li>
                <li class="list-group-item">
                    <tnormhead>RAM: </tnormhead>
                    <tnorm> 4GB</tnorm>
                </li>
                <li class="list-group-item">
                    <tnormhead>Mainboard: </tnormhead>
                    <tnorm> GA-F2A78M-HD2 (rev. 3.1)</tnorm>
                </li>
                <li class="list-group-item">
                    <tnormhead>Gesamtspeicherplatz: </tnormhead>
                    <tnorm> > 8TB</tnorm>
                </li>
            </ul>
        </div>
        <div id="otherlistbox">
            <ul class="list-group">
                <li class="list-group-item">
                    <tnormhead>Letztes OS-Update: </tnormhead>
                    <tnorm> 01.01.2017</tnorm>
                </li>
                <li class="list-group-item">
                    <tnormhead>Letztes FreeMind-Update: </tnormhead>
                    <tnorm> 01.01.2017</tnorm>
                </li>
                <li class="list-group-item">
                    <tnormhead>Letzte Ausführung Papierkorb-Skript: </tnormhead>
                    <tnorm> 01.01.2017</tnorm>
                </li>
                <li class="list-group-item">
                    <tnormhead>Letztes Backup: </tnormhead>
                    <tnorm> 01.01.2017</tnorm>
                </li>
            </ul>
        </div>
    </div>
    <div id="headlinebox">
        <t2>Speicherübersicht:</t2>
        <div id="mainmemorybox">
            <div id="firstmemorybox">
                <div class="c100 p<?php echo $mem[0]; ?> .big.<?php echo $color[0]; ?>">
                    <span>
                      <?php
                      echo $mem[0];
                      echo " %";
                      ?>
                    </span>
                    <div class="slice">
                        <div class="bar"></div>
                        <div class="fill"></div>
                    </div>
                </div>
                <div id="centertextboxmemory">
                    <tmemory><?php echo $name[0]; ?></tmemory>
                </div>
            </div>
            <div id="othermemorybox">
                <div class="c100 p<?php echo $mem[1]; ?> .big.<?php echo $color[1]; ?>">
                    <span>
                      <?php
                      echo $mem[1];
                      echo " %";
                      ?>
                    </span>
                    <div class="slice">
                        <div class="bar"></div>
                        <div class="fill"></div>
                    </div>
                </div>
                <div id="centertextboxmemory">
                    <tmemory><?php echo $name[1]; ?></tmemory>
                </div>
            </div>
            <div id="othermemorybox">
                <div class="c100 p<?php echo $mem[2]; ?> .big.<?php echo $color[2]; ?>">
                    <span>
                      <?php
                      echo $mem[2];
                      echo " %";
                      ?>
                    </span>
                    <div class="slice">
                        <div class="bar"></div>
                        <div class="fill"></div>
                    </div>
                </div>
                <div id="centertextboxmemory">
                    <tmemory><?php echo $name[2]; ?></tmemory>
                </div>
            </div>
            <div id="othermemorybox">
                <div class="c100 p<?php echo $mem[3]; ?> .big.<?php echo $color[3]; ?>">
                    <span>
                      <?php
                      echo $mem[3];
                      echo " %";
                      ?>
                    </span>
                    <div class="slice">
                        <div class="bar"></div>
                        <div class="fill"></div>
                    </div>
                </div>
                <div id="centertextboxmemory">
                    <tmemory><?php echo $name[3]; ?></tmemory>
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
        <a class="btn btn-default" href="#" role="button">Dateisysteme prüfen</a>
        <a class="btn btn-default" href="#" role="button">Festplatten prüfen</a>
    </div>
</body>

</html>
