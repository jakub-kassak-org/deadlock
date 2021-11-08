<?php
set_time_limit(150);
if (session_status() == PHP_SESSION_NONE) {
    session_start();
}
if (isset($_POST['odhlas'])) { // bol odoslany formular s odhlasenim
    unset($_SESSION["user"]);
}
include_once("functions/functions.php");
include_once("localization/localization.php");
if (!isValidLogin()) {
    if(isset($_SESSION["user"])) {
        unset($_SESSION["user"]);
        header('Location: index.php?error=0');
    }
    else{
        header('Location: index.php?error=1');
    }
    die();
}
$user = unserialize($_SESSION["user"]);
if (!isset($_SESSION["lang"]) || isset($_POST["slovak"]))
    $_SESSION["lang"] = "sk";
if (isset($_POST["english"])) {
    $_SESSION["lang"] = "en";
} ?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?php echo $title; ?></title>
    <link href="styly.css" rel="stylesheet">
    <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
    <link rel="icon" href="logo.png">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <link rel="stylesheet" href="multislect/jquery.dropdown.css">
    <script src="multislect/jquery.dropdown.js"></script>
</head>
<body class="pb-5">
<header class="mb-1">
    <div class="container-fluid">
        <div class="row">
            <div class="col-6 col-xl-8">
                <h1 style="display: inline-block;">Deadlock</h1>
            </div>
            <div class="col-xl-1 mt-1 col-3">
                <form method="post">
                    <input type="submit" <?php if ($_SESSION["lang"] == "en") echo "disabled style='color: #FFFFFF'" ?>
                           class="btn btn-link mn-2" value="EN" name="english">
                    <input type="submit" <?php if ($_SESSION["lang"] == "sk") echo "disabled style='color: #FFFFFF'" ?>
                           class="btn btn-link mn-2" value="SK" name="slovak">
                </form>
            </div>
            <?php
            echo '<div class="col-3">';
            echo '<form method="post" style="display: inline-block; float: right; margin-top: 1ex;"> 
			<p> 
			  <input name="odhlas" type="submit" class="btn btn-outline-light mr-1" id="odhlas" value="'.localization_log_out().'"> 
			</p> 
		  </form> 
		  <span class="mr-1 mt-3 text-light d-none d-xl-inline-block">'. localization_logged_in_as(). '<a href="cardHolder.php?id='.$user->id.'">' . $user->first_name . " " . $user->last_name . '</a></span>';
            ?>
        </div>
    </div>
    </div>
</header>
<nav class="navbar-light navbar-expand-sm fixed-top nav" style="background-color: #999999;">
    <button class="navbar-toggler btn btn-outline-secondary" type="button" data-toggle="collapse"
            data-target="#navigation">
        <span class="navbar-toggler-icon"></span></button>
    <div class="collapse navbar-collapse" id="navigation">
        <ul class="navbar-nav">
            <li class="nav-item"><a class="nav-link"
                                    href="rooms.php" <?php if ($menuactive == "rooms") echo 'style="background-color: #000000; color: #FFFFFF;"' ?>><?php echo localization_menu_aps() ?></a>
            </li>
            <li class="nav-item"><a class="nav-link"
                                    href="cards.php" <?php if ($menuactive == "cards") echo 'style="background-color: #000000; color: #FFFFFF;"' ?>><?php echo localization_menu_cards() ?></a>
            </li>
            <li class="nav-item"><a class="nav-link"
                                    href="groups.php" <?php if ($menuactive == "groups") echo 'style="background-color: #000000; color: #FFFFFF;"' ?>><?php echo localization_menu_groups() ?></a>
            </li>
        </ul>
    </div>
</nav>
