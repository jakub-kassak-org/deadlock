<?php
if (session_status() == PHP_SESSION_NONE) {
    session_start();
}
include_once("functions/functions.php");
include_once("functions/service.php");
if(!isValidStaffUser()) {
    header('Location: index.php?error=1');
    die();
}
//echo $_POST["admin"];
$result = editUser($_POST["id"], $_POST["fname"], $_POST["lname"], $_POST["cnr"], isset($_POST["admin"]), $_POST["username"], isset($_POST["disabled"]),);
echo header('Location: cards.php?');

