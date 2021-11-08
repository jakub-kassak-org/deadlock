<?php
if (!isset($_GET["id"])) {
    header('Location: rooms.php');
    die();
}
include_once("functions/service.php");
$result=delete_ap_with_id($_GET["id"]);
header('Location: rooms.php');