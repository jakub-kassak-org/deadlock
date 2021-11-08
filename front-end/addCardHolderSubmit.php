<?php
if (!isset($_POST["submit"]) || !isset($_POST["fname"]) || !isset($_POST["lname"]) || !isset($_POST["cnr"])) {
    header('Location: cards.php');
    die();
}
include_once("functions/service.php");
$result=create_user($_POST["username"], $_POST["fname"], $_POST["lname"], $_POST["cnr"], isset($_POST["admin"]));
if($result)
    header('Location: cardHolder.php?id='.$result->id);