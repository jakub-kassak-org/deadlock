<?php
if (!isset($_GET["id"])) {
    header('Location: cards.php');
    die();
}
include_once("functions/service.php");
$result=delete_user_with_id($_GET["id"]);
header('Location: cards.php');